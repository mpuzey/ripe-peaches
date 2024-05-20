# Ripe peaches
### :peach: Fresh fruit for rotting vegetables :peach:

This is a WIP for an album review aggregator which will follow the rotten tomatoes style thumbs up/ thumbs down aggregation model for album reviews. 
There will be a strong focus on curation of quality publications from which reviews will be drawn. The project will initially rely on web scraping to collect recent reviews.

## Build instructions

This application runs on docker.

#### Prerequisites

For MacOS users:
* Docker for Mac v 17.06 - 17.12
* A recent installation of nodeJS (~v8.8.1a t time of writing)


For linux distributions (untested):
* A recent Docker installation  
* A recent installation of nodeJS (~v8.8.1 at time of writing)


#### Run ripe peaches 

```
./run.sh app
```   
   
## Dev setup
This project is in an early stage of development. The instructions for setting
up the basic Dev tools are as follows:
* Install python 3.9 using the appropriate tooling for your OS. Hitchhikers guide have some good documentation around this
 such as [Installing python 3.9 on OSX](http://docs.python-guide.org/en/latest/starting/install3/osx/).
* Install the project dependencies:
```
pip3 install -r requirements.txt
``` 
* Run all jobs and the server:
```
python3 main.py
```
The server will log some basic information about where we're pulling data during the startup action
of collecting review data. Further down the line the collection and aggregation jobs will always run "out of band" to the
core application and will place our data in some storage backend so that the UI may present it.
* Browse to the root of the project at [localhost:8888](http://localhost:8888)
* Once the server has scraped data from the third party sites you can retrieve it from 
[localhost:8888/reviews](http://localhost:8888/reviews)
* You can run the server in the IDE of your choice such as the community edition of [PyCharm](https://www.jetbrains.com/pycharm/). 
In the case of PyCharm, ensure that your Python 3.6 install is selected as the project interpreter.


### Run the web app only

If you have already run the jobs (see Dev setup) at least once before to pull the latest reviews you can run the `service.py` 
found in `src/app/`. This will start the app only without blocking on the much more time-consuming jobs first. 
  
### Run the tests 

```
python3 -m unittest discover tests/
```
