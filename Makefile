# Detect platform (can be overridden with PLATFORM= env var for CI)
ifndef PLATFORM
ifeq ($(OS),Windows_NT)
    PLATFORM := win-x64
    LIB_EXT := dll
    LIB_NAME := osu.Native.dll
    SED_INPLACE := sed -i
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        PLATFORM := linux-x64
        LIB_EXT := so
        LIB_NAME := osu.Native.so
        SED_INPLACE := sed -i
    endif
    ifeq ($(UNAME_S),Darwin)
        PLATFORM := osx-x64
        LIB_EXT := dylib
        LIB_NAME := osu.Native.dylib
        SED_INPLACE := sed -i ''
    endif
endif
endif

BUILD_DIR   := osu-native/Artifacts/bin/osu.Native/release_$(PLATFORM)
OUTPUT_DIR  := build
PACKAGE_DIR := src/osu_native_py
NATIVE_DIR  := $(PACKAGE_DIR)/native
BIN_DIR     := $(NATIVE_DIR)/bin/$(PLATFORM)
PY_BINDINGS := $(NATIVE_DIR)/bindings.py

.PHONY: all build-osu-native fix-cabinet-header copy-native generate-bindings build build-dist install test test-cov lint type-check clean shell uninstall

all: build-osu-native fix-cabinet-header copy-native install generate-bindings

build-osu-native:
	dotnet publish osu-native/osu.Native -c Release -r $(PLATFORM) -o $(OUTPUT_DIR)/generated
	cp $(BUILD_DIR)/cabinet.h $(OUTPUT_DIR)/generated/cabinet.h

fix-cabinet-header:
	poetry run python scripts/fix_cabinet_header.py

copy-native:
	mkdir -p $(BIN_DIR)
	cp $(OUTPUT_DIR)/generated/$(LIB_NAME) $(BIN_DIR)/

generate-bindings:
	poetry run ctypesgen $(OUTPUT_DIR)/generated/cabinet.h \
		-l $(LIB_NAME) \
		-o $(PY_BINDINGS) \
		-D "bool=char" \
		--allow-gnu-c \
		--no-macro-warnings \
		--no-gnu-types
	@echo "Patching bindings.py for dynamic library loading..."
	@# Replace add_library_search_dirs([]) with a call to get path from environment
	@$(SED_INPLACE) 's|add_library_search_dirs(\[\])|add_library_search_dirs([os.environ.get("OSUPY_LIBRARY_PATH", "")])|' $(PY_BINDINGS)

lint:
	poetry run pre-commit run --all-files

test:
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ -v --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

type-check:
	poetry run mypy .

build:
	@if [ ! -f "$(BIN_DIR)/$(LIB_NAME)" ] || [ ! -f "$(PY_BINDINGS)" ]; then \
		echo "Native library or bindings not found. Run 'make all' first."; \
		exit 1; \
	fi
	poetry build

build-dist: all build

install:
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install --with dev
	poetry run pre-commit install

shell:
	poetry shell

clean:
	rm -rf $(OUTPUT_DIR)
	rm -rf $(NATIVE_DIR)/bin
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

uninstall:
	rm -rf .venv
