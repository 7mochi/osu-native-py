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
        UNAME_M := $(shell uname -m)
        ifeq ($(UNAME_M),aarch64)
            PLATFORM := linux-arm64
        else ifeq ($(UNAME_M),armv7l)
            PLATFORM := linux-arm
        else
            PLATFORM := linux-x64
        endif
        LIB_EXT := so
        LIB_NAME := osu.Native.so
        SED_INPLACE := sed -i
    endif
    ifeq ($(UNAME_S),Darwin)
        PLATFORM := osx-arm64
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

.PHONY: all build-osu-native copy-native generate-bindings generate-test-cases build build-dist install test test-cov lint type-check clean shell uninstall

all: build-osu-native copy-native install generate-bindings generate-test-cases

build-osu-native:
	dotnet publish osu-native/osu.Native -c Release -r $(PLATFORM) -o $(OUTPUT_DIR)/generated

copy-native:
	mkdir -p $(BIN_DIR)
	cp $(OUTPUT_DIR)/generated/$(LIB_NAME) $(BIN_DIR)/

generate-bindings:
	poetry run python scripts/generate_bindings.py --publish $(OUTPUT_DIR)/generated

generate-test-cases:
	mkdir -p $(OUTPUT_DIR)/generated
	dotnet run --project osu-native/osu.Native.Tests -c Release -- $(OUTPUT_DIR)/generated

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
	poetry run python tools/build_all_wheels.py

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
