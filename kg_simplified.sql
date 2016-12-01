SET foreign_key_checks = 0;

-- start from entity
DROP TABLE IF EXISTS Entity;
CREATE TABLE IF NOT EXISTS Entity (
	eid				varchar(20) 	PRIMARY KEY,-- What's the diff to text? Or 20 -> 10?
	label 			varchar(150),		-- only record en.
	description 	varchar(250),
	type			varchar(20) 		not null
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
	datatype		varchar(20) 	not null,
	FOREIGN KEY (eid) REFERENCES entity (eid)
);

-- -- Fingerprint
-- DROP TABLE IF EXISTS Label;
-- CREATE TABLE IF NOT EXISTS Label (
-- 	eid				varchar(20),
-- 	language		varchar(15),
-- 	value 			varchar(150),
-- 	FOREIGN KEY (eid) REFERENCES Entity (eid)
-- );

-- DROP TABLE IF EXISTS Description;
-- CREATE TABLE IF NOT EXISTS Description (
-- 	eid				varchar(20),
-- 	language		varchar(15),
-- 	value 			VARCHAR(250),
-- 	FOREIGN KEY (eid) REFERENCES Entity (eid)
-- );

DROP TABLE IF EXISTS Alias;
CREATE TABLE IF NOT EXISTS Alias (
	eid				varchar(20),
	language		varchar(15),
	value 			varchar(150),
	FOREIGN KEY (eid) REFERENCES Entity (eid)
);

-- Claim
DROP TABLE IF EXISTS Claim;
CREATE TABLE IF NOT EXISTS Claim (
	cid				varchar(60) 		PRIMARY KEY,
	eid				varchar(20)			not null,
	property		varchar(20)			not null,
	value 			varchar(250), -- a representative value for faster access
	FOREIGN KEY (eid) REFERENCES Entity (eid),
	FOREIGN KEY (property) REFERENCES Property (eid)
);

-- Note that Qualifier do not have `type` field
DROP TABLE IF EXISTS Qualifier;
CREATE TABLE IF NOT EXISTS Qualifier ( -- Shall we join the claim/qualifiers?
	qid 			char(40) 		PRIMARY KEY, -- For hash!
	property		varchar(20)		not null,
	value 			varchar(250), -- a representative value for faster access
	FOREIGN KEY (property) REFERENCES Property (eid)
);

DROP TABLE IF EXISTS Cqmapping;
CREATE TABLE IF NOT EXISTS Cqmapping(
	cid				varchar(60),
	qid				char(40),
	FOREIGN KEY (cid) REFERENCES Claim(cid),
	FOREIGN KEY (qid) REFERENCES Qualifier(qid)
);

DROP TABLE IF EXISTS Correlation;
CREATE TABLE IF NOT EXISTS Correlation(
	eid				varchar(20)			not null,
	weid			varchar(20)			not null,
	cid 			varchar(60)		not null,
	FOREIGN KEY (eid) REFERENCES Entity (eid),
	FOREIGN KEY (weid) REFERENCES Entity (eid),
	FOREIGN KEY (cid) REFERENCES Claim (cid)
);

DROP TABLE IF EXISTS Preced;
CREATE TABLE IF NOT EXISTS Preced(
	eid				varchar(20)			not null,
	weid			varchar(20)			not null,
	FOREIGN KEY (eid) REFERENCES Entity (eid),
	FOREIGN KEY (weid) REFERENCES Entity (eid)
);

