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

Run the web app:
```bash
cd web/
python run.py
```
Remember to set up the sql connection in `web/app/src/query_api.py`

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

- [x] Loading event.
- [ ] NLQ: several small queries
- [ ] Qualifier in query

- [ ] Website build for listen 
- [ ] Tree: Some "instance of" not included! Type "Fantasy" (依然范特西) Many entities fail to find any tree entity...
- [ ] Co-occurred: Sort in eid order!
- [ ] Statements: Sort them in Property order!
- [ ] NLQ: Find_claim_value(eid, pid) is needed!
- [ ] Add "#properties" in table "entity" for choosing from name.
## Note

Wikidata can be retrieved [here](http://adapt.seiee.sjtu.edu.cn/~frank/wikidata-latest-all.json.bz2), which is approx 4.5G in compressed form, 80G when extracted.


Currently at 2450000