import json
import cPickle, os, sys, time
__author__ = "hunter"

if __author__ == "hunter":
    import MySQLdb as mysql
    pwd = "1234"
    fpath = "C:/Users/t-honlin/Desktop/wikidata.json"
else:
    import mysql.connector as mysql
    pwd = "listen"

dbname = "wikidata_simplified2"

def init_mysql():
    global cur, db
    # First extend the max_packet size.
    db = mysql.connect(host="localhost", user="root", passwd=pwd, db=dbname,\
        charset="utf8")
    cur = db.cursor()
    cur.execute("SET GLOBAL net_buffer_length = %s" % 1000000)
    cur.execute("SET GLOBAL max_allowed_packet = 1000000000")
    db.commit()
    # The command is on for next connection.
    db = mysql.connect(host="localhost", user="root", passwd=pwd, db=dbname,\
        charset="utf8")
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("SET NAMES 'utf8'")
    db.commit()

def get_valid_properties(fname):
    prop_dict = {}
    f = open(fname)
    for line in f.readlines():
        line = line.decode("utf8").strip().split("\t")
        pid = line[0]
        prop_dict[pid] = line[-1]
    f.close()
    return prop_dict

def query_id_from_name(name):
	# only one
	sql = "select eid from Entity where label = \"%s\"" % name
	print sql
	cur.execute(sql)
	data = cur.fetchone()
	return data[0]

def query_id_from_alias(alias):
	sql = "select eid from Alias where alias = \"%s\"" % alias
	print sql
	cur.execute(sql)
	data = cur.fetchone()
	return data[0]

def query_name_from_id(id):
	sql = "select label from Entity where eid = \"%s\"" % id
	print sql
	cur.execute(sql)
	data = cur.fetchone()
	return data[0]

def query_description_from_id(id):
	sql = "select description from Entity where eid = \"%s\"" % id
	print sql
	cur.execute(sql)
	data = cur.fetchone()
	return data[0]

def query_entities_from_name(name):
	sql = "select eid,label,description from Entity where label = \"%s\"" % name
	print sql
	cur.execute(sql)
	data = cur.fetchall()
	data = [list(x) for x in data]
	return data

def query_entities_from_id(id):
	sql = "select eid,label,description from Entity where eid = \"%s\"" % id
	print sql
	cur.execute(sql)
	data = cur.fetchall()
	data = [list(x) for x in data]
	return data


def query_preceding_categories(eid, detail = True):
	# detail is bool
	cur.execute("select weid from Preced where eid = \"%s\"" % eid)
	weid_set = cur.fetchall()

	query_results = []
	if detail:
		for weid in weid_set:
			# print weid,"weid"
		# I plan to create index of label.
			cur.execute("select label from Entity where eid = \"%s\"" % weid)
			res = cur.fetchall()
			if len(res) > 0:
				res = res[0][0]
				query_results.append(weid[0]+" "+res)
			else:
				query_results.append(weid[0])
		return query_results	
	else:
		return weid_set
	

def query_entity_cooccured(eid):
	global cur
	cur.execute("select distinct(weid) from Correlation where eid = \"%s\"" % eid)
	eset1 = cur.fetchall()
	cur.execute("select distinct(eid) from Correlation where weid = \"%s\"" % eid)
	eset2 = cur.fetchall()
	res = eset1 + eset2
	res = [x[0] for x in res]
	return list(set(res))

def query_statements_properties(eid):
	# all statement
	global prop_dict,cur
	cur.execute("select cid,property,value from Claim where eid = \"%s\"" % eid)
	res = cur.fetchall()
	query_results = []
	for cid,p,v in res:
		# statement = []
		pname = prop_dict[p]
		cur.execute("select qid from Cqmapping where cid = \"%s\"" % cid)
		qid_set = cur.fetchall()
		# print v
		v = convert_entity_to_name(v)
		# print v
		# print v
		statement = [pname,v]
		# statement = statement + pname + " " + v + " "
		for qid in qid_set:
			cur.execute("select property,value from Qualifier where qid = \"%s\"" % qid)
			qp,qv = cur.fetchone()
			qv = convert_entity_to_name(qv)
			statement = statement + [prop_dict[qp],qv]
		query_results.append(statement)

	return query_results


def convert_entity_to_name(eid):
	# took it as the entity. =.=
	global cur
	if eid[0] == 'Q':
		sql = "select label from Entity where eid = \"%s\"" % eid
		# print sql,eid
		cur.execute(sql)
		res = cur.fetchall()
		if len(res) > 0:
			return res[0][0] # the first one and the first element
		else:
			return eid+" (Not found) "
	else:
		return eid

def tree_search(eid):
	sql = "select lft,rgt from htree where eid = \"%s\"" % eid
	cur.execute(sql)
	res = cur.fetchall()
	print res
	sql = "select eid from htree where lft < %s and rgt > %s"
	result = []
	for lft,rgt in res:
		print lft,rgt
		cur.execute(sql)
		result = result + cur.fetchall()
	result = [x[0] for x in result]
	return result

def recursive_search(eid, eid_set):
	sql = "select weid from Preced where eid = \"%s\"" % eid
	cur.execute(sql)
	res = cur.fetchall()
	for weid in res:
		eid_set.append(weid[0])
		recursive_search(weid[0],eid_set)

# Query1: given a name, find corresponding entities.
def find_entity(ename):
    """Return like a list of [eid, label, description]"""
    # data = [
    #     ["P1", "HAH", "HAHA"]
    # ]
    return query_entities_from_name(ename)
    # return data

# Query2: given a eid, find corresponding tree structure.
def find_tree(eid):
    """Return like a list of [eid, label, description, (layer)?]"""
    # data = [
    #     ["P1", "HAH", "HAHA"]
    # ]
    # recursive search

    eid_set = []
    recursive_search(eid, eid_set)
    data = []
   

    #tree search

    # eid_set = tree_search(eid)

	for id in eid_set:
    	data = data + query_entities_from_id(id)

    # return data


# Query3: given a eid, find all coocurred entites.
def find_cooccur(eid):
    """Return like a list of [obj_id, obj_value, pid, pvalue]"""
    
    # data = [
    #     ["P1", "HAH", "HAHA"]
    # ]
    data = []
    eid_set = query_entity_cooccured(eid)
    for id in eid_set:
    	data = data + query_entities_from_id(id)

    return data


# Query4: given a eid, find all its statement and properties.
def find_statements(eid):
    """Return like a list of [pid, pvalue, datavalue,\
         qualifer_pid, qualifier_pvalue, qualifer_datavalue]"""
    # data = [
    #     ["P1", "HAH", "HAHA"]
    # ]
    

    return query_statements_properties(eid)


# Add: given the name, only find its id. If multiple, only choose the first one.
def find_entityid(ename):
    # eid = "Q1"
    # prompt = ""

    return query_id_from_name(ename)

# Add: given a name, find its entity id based on Alias! Only return the first one.
def find_aliasid(alias):
    """Take the first one if many applies"""
    # eid = "Q1"
    # prompt = ""
    return query_id_from_alias(alias)

# Add: given a eid, find its name.
def find_name(eid):
    # name = "ha"
    # prompt = ""
    return query_name_from_id(eid)

# Add: given a eid, find its description.
def find_description(eid):
    # desc = "desc"
    # prompt = ""
    return query_description_from_id(eid)

# Add: given a eid, and prop_id, find the corresponding datavalue.
# if the datavalue is eid, select its label additionally.
# def find_claim(eid, pid):
#     claim = "claim"
#     prompt = ""
#     return claim


init_mysql()

# query 1
print "query 1"
start = time.time()
print query_entities_from_name('Aleksandr Chudakov')
print time.time() - start

# query 2
print "query 2"
start = time.time()
print query_preceding_categories("Q1372409");
print time.time() - start

# query 3
print "query 3"
start = time.time()
print query_entity_cooccured("Q1372409")
print time.time() - start


prop_dict = get_valid_properties("./properties.txt")
# query 4
print "query 4"
start = time.time()
print query_statements_properties("Q1372409")
print time.time() - start
