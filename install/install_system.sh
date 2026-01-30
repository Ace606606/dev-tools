#!/bin/bash
apt update && apt install -y \
    build-essential cmake git gdb lldb \
    clang clangd clang-format clang-tidy \
    cppcheck pkg-config make \
    bash-completion curl wget openssh-client \
    shfmt valgrind \
#    python3 python3-pip python3-venv \
#    libprotobuf-dev libgrpc++-dev libgrpc-dev libprotoc-dev