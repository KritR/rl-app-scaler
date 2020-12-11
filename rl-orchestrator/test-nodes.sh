#!/bin/sh
echo "GET http://localhost:5000/" | ./vegeta attack -duration=5s | ./vegeta report -type=json
