#!/bin/bash

set -e

# perform git pull
pushd /root/cemu
git pull --recurse-submodules
popd

# remove build directory
[[ -d /root/cemu/build ]] && rm -rf /root/cemu/build

# build cemu
pushd /root/cemu
cmake -S . -B build -DCMAKE_BUILD_TYPE=release -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -G Ninja
cmake --build build
popd

strip /root/cemu/bin/Cemu_release
rsync -vr --delete --exclude='.gitignore' /root/cemu/bin/ /output/
