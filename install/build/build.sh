#!/bin/bash

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

SRC_DIR="$REPO_ROOT/scripts/cpp/src"
DST_DIR="$REPO_ROOT/scripts/cpp/dst"

mkdir -p "$DST_DIR"

g++ -std=c++17 -Wall -Wextra -Werror -O3 \
	"$SRC_DIR/vscode_config_manager/vscode_config_manager.cpp" \
	-o "$DST_DIR/vscode_config_manager"

g++ -std=c++17 -Wall -Wextra -Werror -O3 \
	"$SRC_DIR/print_directory_structure/print_directory_structure.cpp" \
	-o "$DST_DIR/print_directory_structure"

if [ $? -eq 0 ]; then
	echo "Build successful! Binaries are in $DST_DIR"
else
	echo "Build failed"
	exit 1
fi
