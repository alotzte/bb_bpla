#!/bin/bash

TAR_FILE="bpla_0_0_22.tar"

docker load -i "$TAR_FILE"

docker images
