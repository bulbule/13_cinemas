# Cinemas

The script takes a list of movies with the corresponding number of cinemas, where they are currently showed, from [here](https://www.afisha.ru/msk/schedule_cinema/) and prints first 10 items of its sorted version. The list can be either sorted by the number of cinemas or by the rating. Thus, the output contains the movie title, its rating and votes (taken from [here](https://www.kinopoisk.ru)) and the number of cinemas. The only drawback is that [kinopoisk](https://www.kinopoisk.ru) does not like parsing and bans your IP. In that case, zeros will be printed out for the rating and votes.

To run, install the requirements:
```#!bash
$ pip install -r requirements.txt
```
# Usage
The default sorting is by rating, which you can get by running:
```#!bash
$ python cinemas.py
```
Otherwise, use an optional parameter `-c`, or `--cinemas` to get sorting by the number of cinemas:
```#!bash
$ python cinemas.py -c
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
