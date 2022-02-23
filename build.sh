#!/bin/sh
pipreqs . --encoding=utf8 --force
docker build --network=host -t plugins:1.1.3 .
docker save -o plugins.tar plugins:1.1.3
docker rmi plugins:1.1.3