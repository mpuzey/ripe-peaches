#!/bin/bash
#set -e

function app() {
    local apiKey=$1

    pushd client
    npm install && npx webpack
    popd

    docker build . -t tmdb-search
    docker rm -f tmdb-search
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