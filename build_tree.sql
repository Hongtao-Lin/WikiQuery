CREATE table num_child (eid varchar(20) NOT NULL, nc int NOT NULL);

CREATE table ancestor (eid varchar(20) NOT NULL);

CREATE table htree (eid varchar(20) NOT NULL, lft int NOT NULL, rgt int not NULL);
CREATE INDEX LFT_RGT on htree(lft,rgt);
CREATE INDEX TREE_INDEX on htree(eid);

insert into num_child (select weid,count(*) from Preced group by weid);
insert into ancestor (select eid from num_child where eid not in (select distinct(eid) from Preced));