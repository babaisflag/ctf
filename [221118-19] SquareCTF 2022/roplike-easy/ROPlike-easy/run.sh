#!/bin/bash

docker build . -t roplikeeasy
docker run -d -p ${HOST_PORT}:8000 roplikeeasy
