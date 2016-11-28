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
	pvalue 			varchar(128),
	rank			smallint, -- Use 0,1,2 -> preferred, normal, deprecated
	datatype		text,
	valuetype		text,
	value 			text, -- a representative value for faster access
	did 			int,
	FOREIGN KEY (eid) REFERENCES Entity (eid),
	FOREIGN KEY (property) REFERENCES Property (eid)
	-- FOREIGN KEY (did) REFERENCES Datavalue (did)
);