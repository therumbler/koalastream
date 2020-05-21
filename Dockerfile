ARG IMAGE=amd64/debian:10.4-slim

FROM $IMAGE as builder

ARG NASM_VERSION=2.14.02
ARG LAME_VERSION=3.100
ARG NGINX_VERSION=1.18.0
ARG NGINXRTMP_VERSION=1.2.1
ARG PYTHON_VERSION=3.8.2
ARG FFMPEG_VERSION=4.1.5

ENV SRC="/usr/local/"

RUN apt-get update && \
    apt-get install -y \
        pkg-config \
        curl \
        libpcre3-dev \
        libtool \
        libssl-dev \
        zlib1g-dev \
        libasound2-dev \
        build-essential \
        libffi-dev

# nginx-rtmp
RUN mkdir -p /dist && cd /dist && \
    curl -OL "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" && \
    tar -xvz -f "nginx-${NGINX_VERSION}.tar.gz" && \
    curl -OL "https://github.com/arut/nginx-rtmp-module/archive/v${NGINXRTMP_VERSION}.tar.gz" && \
    tar -xvz -f "v${NGINXRTMP_VERSION}.tar.gz" && \
    sed -i"" -e '/case ESCAPE:/i /* fall through */' nginx-rtmp-module-${NGINXRTMP_VERSION}/ngx_rtmp_eval.c && \
    cd nginx-${NGINX_VERSION} && \
    ./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-http_v2_module --add-module=/dist/nginx-rtmp-module-${NGINXRTMP_VERSION} && \
    make -j$(nproc) && \
    make install

# nasm
RUN mkdir -p /dist && cd /dist && \
    curl -OL "https://www.nasm.us/pub/nasm/releasebuilds/${NASM_VERSION}/nasm-${NASM_VERSION}.tar.xz" && \
    tar -xvJ -f nasm-${NASM_VERSION}.tar.xz && \
    cd nasm-${NASM_VERSION} && \
    ./configure && \
    make -j$(nproc) && \
    make install

# x264
RUN mkdir -p /dist && cd /dist && \
    curl -OL https://code.videolan.org/videolan/x264/-/archive/stable/x264-stable.tar.bz2 && \
    tar -xvj -f x264-stable.tar.bz2 && \
    cd x264-stable && \
    ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --enable-shared && \
    make -j$(nproc) && \
    make install

# libmp3lame
RUN mkdir -p /dist && cd /dist && \
    curl -OL "https://downloads.sourceforge.net/project/lame/lame/${LAME_VERSION}/lame-${LAME_VERSION}.tar.gz" && \
    tar -xvz -f lame-${LAME_VERSION}.tar.gz && \
    cd lame-${LAME_VERSION} && \
    ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --disable-static --enable-nasm && \
    make -j$(nproc) && \
    make install

# ffmpeg
RUN mkdir -p /dist && cd /dist && \
    curl -OL "https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz" && \
    tar -xvz -f ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    cd ffmpeg-${FFMPEG_VERSION} && \
    ./configure \
        --bindir="${SRC}/bin" \
        --extra-cflags="-I${SRC}/include" \
        --extra-ldflags="-L${SRC}/lib" \
        --prefix="${SRC}" \
        --enable-nonfree \
        --enable-gpl \
        --enable-version3 \
        --enable-libmp3lame \
        --enable-libx264 \
        --enable-openssl \
        --enable-postproc \
        --enable-small \
        --enable-static \
        --disable-debug \
        --disable-doc \
        --disable-shared && \
    make -j$(nproc) && \
    make install

# python
RUN cd /dist
RUN curl -OL "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz"
RUN tar -xf "Python-${PYTHON_VERSION}.tar.xz"
WORKDIR Python-${PYTHON_VERSION}/
RUN ls
RUN ./configure --enable-optimizations
RUN make -j$(nproc)
RUN make install
RUN python3 -m pip install pipenv


WORKDIR /koalastream

COPY conf/nginx.conf /koalastream/conf/nginx.conf
COPY run.sh /koalastream/run.sh



RUN mkdir /app
WORKDIR /app
COPY Pipfile* ./

RUN pipenv sync
COPY . /app

CMD "./run.sh"