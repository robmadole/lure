#!/bin/bash
cd /tmp
mkdir src
cd src
git clone --depth=1 -b v0.21.0 https://github.com/libgit2/libgit2.git
cd libgit2
mkdir build
cd build
cmake .. -DBUILD_CLAR=OFF
cmake --build . --target install
