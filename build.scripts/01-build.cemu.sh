#!/bin/bash
 
mkdir -p /root/cemu/build
pushd /root/cemu/build
cmake .. -DCMAKE_BUILD_TYPE=debug -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -G Ninja -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON -DCMAKE_MAKE_PROGRAM=/usr/bin/ninja
ninja
popd
strip /root/cemu/bin/Cemu
rsync -avr --delete /root/cemu/bin/ /output/
