#!/usr/bin/env bash

image=${REGISTRY}/orderly-web-user-cli:master
docker run -v montagu_orderly_volume:/orderly --network ${NETWORK} $image $@