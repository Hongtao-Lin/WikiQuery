# Introduction

This is the database course project, which is about storing information in wikidata in SQL schemas. 

It requires smart design on database schema, and possible optimization by indexing.

By implementing required queries and possible natural language queries, the database is essientially served as a knowledge graph.

To demonstrate the work, a web GUI will be designed and implemented.

# Architecture

```
.
├── data
│   └── wikidata-latest-all.json  	# omited due to large in size
├── web								# GUI display 
├── util							# possible util functions 
└── README.md 						
```

# Note

wikidata can be retrieved [here](http://adapt.seiee.sjtu.edu.cn/~frank/wikidata-latest-all.json.bz2), which is approx 4.5G in compressed form, 80G when extracted.
