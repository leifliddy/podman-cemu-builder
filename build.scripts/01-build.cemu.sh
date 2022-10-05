#!/bin/bash
 
# perform git pull
pushd /root/cemu
git pull --recurse-submodules
popd 

# build cemu
mkdir -p /root/cemu/build
pushd /root/cemu/build
cmake .. -DCMAKE_BUILD_TYPE=release -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -G Ninja
cmake --build .
popd
strip /root/cemu/bin/Cemu
rsync -vr --delete --exclude='.gitignore' /root/cemu/bin/ /output/
