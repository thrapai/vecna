#!/bin/bash
set -e

isort $*
black $*
pylint $*
# pytest --doctest-modules $*
