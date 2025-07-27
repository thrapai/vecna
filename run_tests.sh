#!/bin/bash
set -e

coverage run -m pytest --doctest-modules tests/ "$@"

coverage report -m
