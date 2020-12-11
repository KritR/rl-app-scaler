#!/bin/bash
docker ps | grep app-agent | awk '{print $NF;}' | xargs -I{} docker stop -t 0 {}
