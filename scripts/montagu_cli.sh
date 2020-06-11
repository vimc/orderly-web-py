#!/usr/bin/env bash

image=vimc/montagu-cli:master
docker pull $image
exec docker run --network montagu_default $image "$@"