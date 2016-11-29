# WikiQuery

## Introduction

This is the database course project, which is about storing information in wikidata in SQL schemas. 

It requires smart design on database schema, and possible optimization by indexing.

By implementing required queries and possible natural language queries, the database is essientially served as a knowledge graph.

To demonstrate the work, a web GUI will be designed and implemented.

## Setup

For SQL table construction, run `kg_simplified.sql` in MySQL.

For data import, run `python preprocess.py`. Note about some global config in it.

For web display, we use [nodejs](https://github.com/nodejs/node) for backend logic, [react-native](https://github.com/facebook/react-native) and [material-ui](https://github.com/callemall/material-ui) for front display: 
```
npm install material-ui
npm install react-tap-event-plugin
npm install --save-dev babel-preset-stage-1

```
See [here](http://www.material-ui.com/#/get-started/installation) for detailed instruction on installation of material-ui.


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