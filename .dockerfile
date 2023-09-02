FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \