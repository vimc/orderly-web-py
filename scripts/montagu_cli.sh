#!/usr/bin/env bash

image=${REGISTRY}/montagu-cli:master
docker pull $image
exec docker run --network ${NETWORK} $image "$@"