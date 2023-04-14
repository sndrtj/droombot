#!/usr/bin/env bash

POETRY=${POETRY_HOME}/venv/bin/poetry
exec "${POETRY}" run droombot "${1}"
