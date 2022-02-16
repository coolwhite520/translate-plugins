#!/bin/sh
pipreqs . --encoding=utf8 --force
docker build --network=host -t plugins:4.2.3 .
docker save -o plugins.tar plugins:4.2.3