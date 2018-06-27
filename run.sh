#!/bin/bash
#set -e

function app() {

    docker build . -t ripe-peaches
    docker rm -f ripe-peaches
    docker run -it --publish 8888:8888 --name ripe-peaches ripe-peaches
}

function clearIntermediateImages() {
    docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
}

function clearAllContainers() {
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
}

$@