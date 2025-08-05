#!/bin/bash
set -e

pytest --cov --cov-branch --doctest-modules tests/ "$@"
