-- start from entity

CREATE TABLE IF NOT EXISTS Entity (
	eid				varchar(20) 	PRIMARY KEY,-- What's the diff to text? Or 20 -> 10?
	pageid			int 			not null,
	ns				smallint 		not null,
	lastrevid		int 			not null,
	modified		char(20) 		not null,
	type			varchar(8) 		not null
);

-- Inheritance: entity/property
CREATE TABLE IF NOT EXISTS Item (
	eid				varchar(20),
	FOREIGN KEY (eid) REFERENCES entity (eid)
);

CREATE TABLE IF NOT EXISTS Property (
	eid				varchar(20),
	datatype		varchar(20) 	not null,
	FOREIGN KEY (eid) REFERENCES entity (eid)
);

-- Sitelink for item
CREATE TABLE IF NOT EXISTS Sitelink (
	eid				varchar(20),
	site 			varchar(20) 	not null,
	title 			varchar(64) 	not null,
	CONSTRAINT pk_Sitelink PRIMARY KEY (site, title),
	FOREIGN KEY (eid) REFERENCES item (eid) -- Any problems here?
);

CREATE TABLE IF NOT EXISTS Badge (
	site 			varchar(20) 	not null,
	title 			varchar(64) 	not null,
	bid				varchar(20) 	not null,
	CONSTRAINT fk_b_s FOREIGN KEY (site, title) REFERENCES Sitelink (site, title)
);

-- Fingerprint

CREATE TABLE IF NOT EXISTS Label (
	eid				varchar(20),
	language		varchar(8),
	value 			varchar(128),
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

CREATE TABLE IF NOT EXISTS Description (
	eid				varchar(20),
	language		varchar(8),
	value 			varchar(128),
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

CREATE TABLE IF NOT EXISTS Alias (
	eid				varchar(20),
	language		varchar(8),
	value 			varchar(128),
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

-- Datavalue

CREATE TABLE IF NOT EXISTS Datavalue (
	did				int 			PRIMARY KEY,
	valuetype		varchar(32) 	not null
);


CREATE TABLE IF NOT EXISTS String ( -- Shall we reserve this type??
	did				int,
	value 			varchar(128),
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

CREATE TABLE IF NOT EXISTS WikiEntityid ( -- Shall we reserve this type??
	did 			int,
	eid				varchar(20),
	FOREIGN KEY (did) REFERENCES Datavalue (did),
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

CREATE TABLE IF NOT EXISTS Globecoordinate (
	did 			int,
	latitude		real 			not null,
	longitude		real 			not null,
	prec			int 			not null,
	globe			varchar(64) 	not null,
	altitude		real,
	FOREIGN KEY (did) REFERENCES Datavalue (did)

);

CREATE TABLE IF NOT EXISTS Quantity (
	did 			int,
	amount			real 			not null,
	upperBound		varchar(32) 	not null,
	lowerBound		varchar(32) 	not null,
	unit			varchar(64) 	not null,
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

CREATE TABLE IF NOT EXISTS Time (
	did 			int,
	value			varchar(32) 	not null,
	timezone		smallint 		not null,
	bef				int 			not null,
	aft				int 			not null,
	prec			int 			not null,
	calendarmodel	varchar(64) 	not null,
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);


-- Claim
CREATE TABLE IF NOT EXISTS Claim (
	cid				char(40) 		PRIMARY KEY, 
	type			varchar(9) 		not null, -- statement or not
	snaktype		varchar(9)		not null,
	-- For snak
	property		varchar(20)		not null,
	rank			smallint, -- Use 0,1,2 -> preferred, normal, deprecated
	datatype		varchar(20),
	valuetype		varchar(20),
	value 			varchar(32), -- a representative value for faster access
	did 			int,
	FOREIGN KEY (property) REFERENCES Property (eid),
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

-- Note that Qualifier do not have `type` field
CREATE TABLE IF NOT EXISTS Qualifier ( -- Shall we join the claim/qualifiers?
	qid 			char(40) 		PRIMARY KEY, -- For hash!
	cid				char(40),
	snaktype		varchar(9)		not null,
	property		varchar(20)		not null,
	rank			smallint, -- Calculated from q_order
	datatype		varchar(20),
	valuetype		varchar(20),
	value 			varchar(32), -- a representative value for faster access
	did 			int 			not null,
	FOREIGN KEY (property) REFERENCES Property (eid),
	FOREIGN KEY (cid) REFERENCES Claim (cid),
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

CREATE TABLE IF NOT EXISTS Reference ( -- Shall we reserve it?
	rid 			char(40) 		PRIMARY KEY -- For hash!
);

CREATE TABLE IF NOT EXISTS ReferneceItem (
	rid				char(40),
	cid				char(40),
	snaktype		varchar(9)		not null,
	property		varchar(20)		not null,
	rank			smallint, -- Calculated from q_order
	datatype		varchar(20),
	valuetype		varchar(20),
	value 			varchar(32), -- a representative value for faster access
	did 			int 			not null,
	FOREIGN KEY (property) REFERENCES Property (eid),
	FOREIGN KEY (cid) REFERENCES Claim (cid),
	FOREIGN KEY (rid) REFERENCES Reference (rid)
);

