#!/bin/bash
set -e

pytest --doctest-modules tests/ $*
