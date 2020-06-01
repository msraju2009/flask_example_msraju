$ cd to folder where it is cloned 
$ docker build -t python-RP-dev .
$ docker run --rm -it -p 8080:8080 python-RP-dev