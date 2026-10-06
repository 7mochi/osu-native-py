from __future__ import annotations

import ctypes
import json
import keyword
import logging
import math
import os
import re
from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace
from pathlib import Path
from textwrap import indent

from ctypesgen.ctypedescs import CtypesSimple
from ctypesgen.ctypedescs import CtypesStruct
from ctypesgen.ctypedescs import CtypesType
from ctypesgen.ctypedescs import CtypesTypedef
from ctypesgen.descriptions import DescriptionCollection
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined


@dataclass(frozen=True)
class Field:
    native_name: str
    annotation: str
    description: str = ""
    default: str | None = None

    @property
    def name(self) -> str:
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", self.native_name)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    @property
    def nullable(self) -> bool:
        return self.annotation.startswith("Optional[")

    @property
    def kind(self) -> str:
        return self.annotation[len("Optional[") : -1] if self.nullable else self.annotation

    @property
    def zero(self) -> str:
        return {"bool": "False", "int": "0", "float": "0.0"}[self.kind]

    @property
    def value(self) -> str:
        value = f"native.{self.native_name}"
        condition = f" if {value}.hasValue else None" if self.nullable else ""
        if self.nullable:
            value += ".value"
        if self.kind.endswith("Attributes"):
            value = f"{self.kind}.from_native({value})"
        return value + condition

    @property
    def nested(self) -> bool:
        return self.kind.endswith("Attributes")


@dataclass
class Model:
    name: str
    fields: list[Field]
    base: str = ""
    inherited: tuple[str, ...] = ()
    converter: str = ""
    handles: list[Field] = field(default_factory=list)
    description: str = ""

    @property
    def own_fields(self) -> list[Field]:
        return [item for item in self.fields if item.name not in self.inherited]

    @property
    def docstring(self) -> str:
        documented = [item for item in self.fields if item.description]
        parts = [self.description] if self.description else []
        if documented:
            entries = [
                indent(item.name + ": " + item.description.replace("\n", "\n    "), "    ")
                for item in documented
            ]
            parts.append("Attributes:\n" + "\n".join(entries))
        return "\n\n".join(parts)


def resolve(ctype: CtypesType, typedefs: dict[str, CtypesType]) -> CtypesType:
    while isinstance(ctype, CtypesTypedef):
        ctype = typedefs[ctype.name]
    return ctype


def annotation(ctype: CtypesType, typedefs: dict[str, CtypesType]) -> str:
    ctype = resolve(ctype, typedefs)
    if isinstance(ctype, CtypesSimple):
        kind = getattr(ctypes, ctype.py_string(), None)
        if kind is not None:
            value_type = type(kind().value)
            if value_type in (bool, int, float):
                return value_type.__name__
    if isinstance(ctype, CtypesStruct):
        if ctype.tag == "ManagedObjectHandle":
            return "bindings.ManagedObjectHandle"
        if re.fullmatch(r"Native\w+(Difficulty|Performance)Attributes", ctype.tag):
            return ctype.tag[len("Native") :]
        members = dict(ctype.members or [])
        if list(members) == ["hasValue", "value"]:
            if annotation(members["hasValue"], typedefs) == "bool":
                return f"Optional[{annotation(members['value'], typedefs)}]"
    raise ValueError(f"Unsupported native field type: {ctype}")


def get_fields(name: str, typedefs: dict[str, CtypesType]) -> list[Field]:
    struct = resolve(typedefs[name], typedefs)
    if not isinstance(struct, CtypesStruct) or struct.members is None:
        raise ValueError(f"Missing native struct: {name}")
    fields = [Field(member, annotation(kind, typedefs)) for member, kind in struct.members]
    names = [item.name for item in fields]
    if len(names) != len(set(names)) or any(keyword.iskeyword(name) for name in names):
        raise ValueError(f"Invalid Python field names: {name}")
    return fields


def get_models(descriptions: DescriptionCollection) -> list[Model]:
    typedefs = {item.name: item.ctype for item in descriptions.typedefs}
    attributes = {
        name[len("Native") :]: get_fields(name, typedefs)
        for name in sorted(typedefs)
        if re.fullmatch(r"Native\w+(Difficulty|Performance)Attributes", name)
    }
    models = []
    for category in ("Difficulty", "Performance"):
        group = {
            name: fields
            for name, fields in attributes.items()
            if name.endswith(category + "Attributes") and not any(item.nested for item in fields)
        }
        if not group:
            raise ValueError(f"No native {category.lower()} attribute exports")
        base = category + "Attributes"
        first = next(iter(group.values()))
        common = [item for item in first if all(item in fields for fields in group.values())]
        inherited = tuple(item.name for item in common)
        models.append(Model(base, common))
        models.extend(
            Model(name, fields, base, inherited, "attributes") for name, fields in group.items()
        )
    names = {model.name for model in models}
    models.extend(
        Model(name, fields, converter="attributes")
        for name, fields in attributes.items()
        if name not in names
    )
    score = get_fields("NativeScoreInfo", typedefs)
    handles = [item for item in score if item.annotation == "bindings.ManagedObjectHandle"]
    values = sorted((item for item in score if item not in handles), key=lambda item: item.nullable)
    models.append(Model("ScoreInfo", values, converter="score", handles=handles))
    return models


def configure_model(model: Model, metadata: dict) -> Model:
    if not isinstance(metadata, dict):
        raise ValueError(f"Invalid metadata for {model.name}")
    unknown = set(metadata) - {"description", "fields", "defaults"}
    names = {item.name for item in model.fields}
    docs = metadata.get("fields", {})
    defaults = metadata.get("defaults", {})
    if any(not isinstance(value, dict) for value in (docs, defaults)):
        raise ValueError(f"Invalid field metadata for {model.name}")
    if any(
        not isinstance(name, str) or not name.isidentifier() or keyword.iskeyword(name)
        for name in set(docs) | set(defaults)
    ):
        raise ValueError(f"Invalid documented field names for {model.name}")
    stale = set(defaults) - names
    if unknown or stale:
        raise ValueError(f"Invalid metadata for {model.name}: {sorted(unknown | stale)}")
    description = metadata.get("description", "")
    if not isinstance(description, str) or any(not isinstance(text, str) for text in docs.values()):
        raise ValueError(f"Invalid documentation for {model.name}")
    if defaults and model.converter != "score":
        raise ValueError(f"Defaults are only supported for ScoreInfo: {model.name}")
    fields = []
    for item in model.fields:
        default = None
        if model.converter == "score":
            kinds = {"bool": bool, "int": int, "float": float}
            if item.kind not in kinds:
                raise ValueError(f"Unsupported score field: {item.native_name}")
            value = defaults.get(item.name, None if item.nullable else kinds[item.kind]())
            if value is None:
                valid = item.nullable
            else:
                valid = type(value) is kinds[item.kind]
                if isinstance(value, float):
                    valid = valid and math.isfinite(value)
            if not valid:
                raise ValueError(f"Invalid default for {model.name}.{item.name}")
            default = repr(value)
        fields.append(replace(item, description=docs.get(item.name, ""), default=default))
    return replace(model, fields=fields, description=description)


def python_docstring(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return '"""' + escaped + '\n"""'


def render_models(models: list[Model], schema: dict) -> dict[str, str]:
    if not isinstance(schema, dict):
        raise ValueError("Model metadata must be an object")
    unknown = set(schema) - {model.name for model in models}
    if unknown:
        raise ValueError(f"Unknown documented models: {sorted(unknown)}")

    models = [configure_model(model, schema.get(model.name, {})) for model in models]
    missing = [
        f"{model.name}.{item.name}"
        for model in models
        for item in model.own_fields
        if not item.description.strip()
    ]
    if missing:
        message = "Missing field documentation: " + ", ".join(missing)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(
                f"::warning file=scripts/models.json,title=Missing field documentation::{message}",
            )
        else:
            logging.getLogger(__name__).warning(message)

    environment = Environment(
        loader=FileSystemLoader(Path(__file__).with_name("templates")),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters["python_docstring"] = python_docstring
    template = environment.get_template("models.py.jinja")
    return {
        "attributes.py": template.render(
            models=[model for model in models if model.name != "ScoreInfo"],
        ),
        "score_info.py": template.render(
            models=[model for model in models if model.name == "ScoreInfo"],
        ),
    }


def generate_models(descriptions: DescriptionCollection) -> dict[str, str]:
    schema = json.loads(Path(__file__).with_name("models.json").read_text(encoding="utf-8"))
    return render_models(get_models(descriptions), schema)
