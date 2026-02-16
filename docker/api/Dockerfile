FROM python:3.12-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


RUN apt update \
    && apt install --no-install-recommends -y tzdata gcc libc-dev libffi-dev python3-dev\
    && apt clean


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /usr/src/api

RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=./api/uv.lock,target=uv.lock \
--mount=type=bind,source=./api/pyproject.toml,target=pyproject.toml \
uv sync --frozen --no-install-project

RUN apt-get install -y wget bash git gcc g++ gfortran  liblapack-dev libamd2 libcholmod3 libmetis-dev libsuitesparse-dev libnauty2-dev
RUN wget -nH https://raw.githubusercontent.com/coin-or/coinbrew/master/coinbrew
RUN chmod u+x coinbrew
RUN bash coinbrew fetch Cbc@master
RUN bash coinbrew build Cbc@master --no-prompt --prefix=/usr/local --tests=none --enable-cbc-parallel
ENV PMIP_CBC_LIBRARY="/usr/local/lib/libCbc.so"
ENV LD_LIBRARY_PATH="/home/haroldo/prog/lib"