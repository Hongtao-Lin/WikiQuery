# WikiQuery

## Introduction

This is the database course project, which is about storing information in wikidata in SQL schemas. 

It requires smart design on database schema, and possible optimization by indexing.

By implementing required queries and possible natural language queries, the database is essientially served as a knowledge graph.

To demonstrate the work, a web GUI will be designed and implemented.

## Setup

For SQL table construction, run `kg_simplified.sql` in MySQL.

For data import, run `python preprocess.py`. Note about some global config in it.

For web display, we use [flask](https://github.com/pallets/flask) for backend logic, [react-js](https://github.com/facebook/react) and [materialize](https://github.com/Dogfalo/materialize) for front display: 



## Architecture

```
.
├── data
│   └── wikidata-latest-all.json  	# omited due to large in size
├── web								# backend logic + GUI display 
├── util							# possible util functions 
├── resource						# other files
└── README.md
```

## TODO

- Change Material-ui svg images at Master Footer!

## Note

wikidata can be retrieved [here](http://adapt.seiee.sjtu.edu.cn/~frank/wikidata-latest-all.json.bz2), which is approx 4.5G in compressed form, 80G when extracted.


Currently at 3628000
Currently at 420000
Currently at 2860000