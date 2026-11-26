linux_arch := if arch() == "x86_64" { "x64" } else if arch() == "aarch64" { "arm64" } else { arch() }
platform := if os() == "windows" { "win-x64" } else if os() == "macos" { "osx-arm64" } else { "linux-" + linux_arch }
lib_name := if os() == "windows" { "osu.Native.dll" } else if os() == "macos" { "osu.Native.dylib" } else { "osu.Native.so" }

output_dir := "build"
package_dir := "src/osu_native_py"
native_dir := package_dir + "/native"
bin_dir := native_dir + "/bin/" + platform
py_bindings := native_dir + "/bindings.py"

bump_author_name := "7mochi-bot"
bump_author_email := "bot@osupe.ru"

default: all

all: build-osu-native copy-native install generate-bindings generate-test-cases

build-osu-native:
    dotnet publish osu-native/osu.Native -c Release -r {{ platform }} -o {{ output_dir }}/generated

copy-native:
    mkdir -p {{ bin_dir }}
    cp {{ output_dir }}/generated/{{ lib_name }} {{ bin_dir }}/

generate-bindings:
    poetry run python scripts/generate_bindings.py --publish {{ output_dir }}/generated

generate-test-cases:
    mkdir -p {{ output_dir }}/generated
    dotnet run --project osu-native/osu.Native.Tests -c Release -- {{ output_dir }}/generated

lint:
    poetry run pre-commit run --all-files

test:
    poetry run pytest tests/ -v

test-cov:
    poetry run pytest tests/ -v --cov-report=html
    echo "Coverage report generated in htmlcov/index.html"

type-check:
    poetry run mypy .

build:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -f "{{ bin_dir }}/{{ lib_name }}" ] || [ ! -f "{{ py_bindings }}" ]; then
        echo "Native library or bindings not found. Run 'just all' first."
        exit 1
    fi
    poetry run python tools/build_all_wheels.py

build-dist: all build

install:
    POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install --with dev
    poetry run pre-commit install

shell:
    poetry shell

clean:
    rm -rf {{ output_dir }}
    rm -rf {{ native_dir }}/bin
    rm -rf .pytest_cache
    rm -rf .coverage
    rm -rf htmlcov
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

uninstall:
    rm -rf .venv

bump part="patch":
    #!/usr/bin/env bash
    set -euo pipefail

    case "{{ part }}" in patch|minor|major) ;; *) echo "usage: just bump [patch|minor|major]" >&2; exit 1 ;; esac

    if [ "$(git branch --show-current)" != master ]; then
        echo "error: just bump must run on master" >&2
        exit 1
    fi

    GIT_AUTHOR_NAME="{{ bump_author_name }}" \
    GIT_AUTHOR_EMAIL="{{ bump_author_email }}" \
    GIT_COMMITTER_NAME="{{ bump_author_name }}" \
    GIT_COMMITTER_EMAIL="{{ bump_author_email }}" \
    poetry run bump-my-version bump {{ part }}

    tag="osu-native-py-v$(poetry version -s)"
    git rev-parse -q --verify "refs/tags/$tag" >/dev/null || {
        echo "error: release tag was not created" >&2
        exit 1
    }

    echo "Created $tag. Review it, then push:"
    echo "  git push origin HEAD $tag"
