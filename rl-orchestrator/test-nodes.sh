#!/bin/sh
echo "GET http://localhost:5000/" | ./vegeta attack -duration=2s | ./vegeta report -type=json
