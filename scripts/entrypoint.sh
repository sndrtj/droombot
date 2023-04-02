#!/usr/bin/env bash

POETRY=${POETRY_HOME}/venv/bin/poetry
${POETRY} run droombot "${1}"
