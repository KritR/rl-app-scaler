#!/bin/sh
docker ps | grep app-agent | awk '{print $13;}' | xargs -I{} docker stop -t 0 {}
