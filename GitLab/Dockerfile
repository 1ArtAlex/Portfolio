FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    cmake \
    make \
    g++ \
    wget \
    unzip

RUN wget https://github.com/google/googletest/archive/release-1.10.0.zip && \
    unzip release-1.10.0.zip && \
    cd googletest-release-1.10.0 && \
    mkdir build && cd build && \
    cmake -DCMAKE_CXX_FLAGS="-Wno-error=maybe-uninitialized" .. && \
    make && \
    make install

COPY . /scr/myapp
WORKDIR /scr/myapp
RUN mkdir build && cd build && \
    cmake .. && \
    make

WORKDIR /scr/myapp/build
CMD ["./run_tests"]


