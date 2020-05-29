#!/bin/bash

ECEL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

for plugin in "$ECEL_DIR"/plugins/collectors/*; do
    if [ -d "$plugin" ]; then
        rm -rf "$plugin"/raw/.M*
        rm -rf "$plugin"/raw/*
        rm -rf "$plugin"/parsed/.M*
        rm -rf "$plugin"/parsed/*
        rm -rf "$plugin"/compressed/.M*
        rm -rf "$plugin"/compressed/*
    fi
done
