SET foreign_key_checks = 0;

-- start from entity
DROP TABLE IF EXISTS Entity;
CREATE TABLE IF NOT EXISTS Entity (
	eid				varchar(20) 	PRIMARY KEY,-- What's the diff to text? Or 20 -> 10?
	label 			text,		-- only record en.
	description 	text,
	type			text 		not null
);

-- Inheritance: entity/property
DROP TABLE IF EXISTS Item;
CREATE TABLE IF NOT EXISTS Item (
	eid				varchar(20),
	FOREIGN KEY (eid) REFERENCES entity (eid)
);

DROP TABLE IF EXISTS Property;
CREATE TABLE IF NOT EXISTS Property (
	eid				varchar(20),
	datatype		text 	not null,
	FOREIGN KEY (eid) REFERENCES entity (eid)
);

-- Sitelink for item
DROP TABLE IF EXISTS Sitelink;
CREATE TABLE IF NOT EXISTS Sitelink (
	eid				varchar(20),
	site 			varchar(128) 	not null,
	title 			varchar(128) 	not null,
	CONSTRAINT pk_Sitelink PRIMARY KEY (site, title),
	FOREIGN KEY (eid) REFERENCES item (eid) -- Any problems here?
);

DROP TABLE IF EXISTS Badge;
CREATE TABLE IF NOT EXISTS Badge (
	site 			varchar(128) 	not null,
	title 			varchar(128) 	not null,
	bid				varchar(20) 	not null,
	CONSTRAINT fk_b_s FOREIGN KEY (site, title) REFERENCES Sitelink (site, title)
);

-- Fingerprint
DROP TABLE IF EXISTS Label;
CREATE TABLE IF NOT EXISTS Label (
	eid				varchar(20),
	language		text,
	value 			text,
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

DROP TABLE IF EXISTS Description;
CREATE TABLE IF NOT EXISTS Description (
	eid				varchar(20),
	language		text,
	value 			text,
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

DROP TABLE IF EXISTS Alias;
CREATE TABLE IF NOT EXISTS Alias (
	eid				varchar(20),
	language		text,
	value 			text,
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

-- Datavalue
DROP TABLE IF EXISTS Datavalue;
CREATE TABLE IF NOT EXISTS Datavalue (
	did				int 	AUTO_INCREMENT 	PRIMARY KEY,
	valuetype		text 	not null
);

DROP TABLE IF EXISTS String;
CREATE TABLE IF NOT EXISTS String ( -- Shall we reserve this type??
	did				int,
	value 			text,
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

DROP TABLE IF EXISTS Monolingualtext;
CREATE TABLE IF NOT EXISTS Monolingualtext ( -- Shall we reserve this type??
	did				int,
	language		text,
	value 			text,
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

DROP TABLE IF EXISTS WikiEntityid;
CREATE TABLE IF NOT EXISTS WikiEntityid ( -- Shall we reserve this type??
	did 			int,
	eid				varchar(20),
	FOREIGN KEY (did) REFERENCES Datavalue (did),
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

DROP TABLE IF EXISTS Globecoordinate;
CREATE TABLE IF NOT EXISTS Globecoordinate (
	did 			int,
	latitude		real 			not null,
	longitude		real 			not null,
	prec			int 			not null,
	globe			text 	not null,
	altitude		real,
	FOREIGN KEY (did) REFERENCES Datavalue (did)

);

DROP TABLE IF EXISTS Quantity;
CREATE TABLE IF NOT EXISTS Quantity (
	did 			int,
	amount			real 			not null,
	upperBound		text 	not null,
	lowerBound		text 	not null,
	unit			text 	not null,
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

DROP TABLE IF EXISTS Time;
CREATE TABLE IF NOT EXISTS Time (
	did 			int,
	value			text 	not null,
	timezone		smallint 		not null,
	bef				int 			not null,
	aft				int 			not null,
	prec			int 			not null,
	calendarmodel	text 	not null,
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);


-- Claim
DROP TABLE IF EXISTS Claim;
CREATE TABLE IF NOT EXISTS Claim (
	cid				varchar(128) 		PRIMARY KEY,	
	eid				varchar(20)			not null,
	evalue			varchar(128),
	type			text 				not null, -- statement or not
	snaktype		text				not null,
	-- For snak
	property		varchar(20)			not null,
	pvalue			varchar(128),
	rank			smallint, -- Use 0,1,2 -> preferred, normal, deprecated
	datatype		text,
	valuetype		text,
	value 			text, -- a representative value for faster access
	did 			int,
	FOREIGN KEY (eid) REFERENCES Entity (eid),
	FOREIGN KEY (property) REFERENCES Property (eid),
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

-- Note that Qualifier do not have `type` field
DROP TABLE IF EXISTS Qualifier;
CREATE TABLE IF NOT EXISTS Qualifier ( -- Shall we join the claim/qualifiers?
	qid 			char(40) 		PRIMARY KEY, -- For hash!
	cid				varchar(128),
	snaktype		text		not null,
	property		varchar(20)		not null,
	rank			smallint, -- Calculated from q_order
	datatype		text,
	valuetype		text,
	value 			text, -- a representative value for faster access
	did 			int,
	FOREIGN KEY (property) REFERENCES Property (eid),
	FOREIGN KEY (cid) REFERENCES Claim (cid),
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

DROP TABLE IF EXISTS ReferenceItem;
CREATE TABLE IF NOT EXISTS ReferenceItem (
	rid				char(40)	PRIMARY KEY,
	snaktype		text		not null,
	property		varchar(20)		not null,
	rank			smallint, -- Calculated from q_order
	datatype		text,
	valuetype		text,
	value 			text, -- a representative value for faster access
	did 			int,
	FOREIGN KEY (property) REFERENCES Property (eid),
	FOREIGN KEY (did) REFERENCES Datavalue (did)
);

DROP TABLE IF EXISTS Reference;
CREATE TABLE IF NOT EXISTS Reference ( -- Shall we reserve it?
	rid 			char(40), -- For hash!
	cid				varchar(128),
	FOREIGN KEY (cid) REFERENCES Claim (cid), 
	FOREIGN KEY (rid) REFERENCES ReferenceItem (rid)
);

