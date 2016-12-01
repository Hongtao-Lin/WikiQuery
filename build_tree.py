import json
import cPickle, os, sys, time
import mysql.connector

def init_mysql():
    global cur, db
    # First extend the max_packet size.
    db = mysql.connector.connect(host="localhost", user="root", passwd="Listen", db="wikidata_simplified",\
        charset="utf8")
    cur = db.cursor()
    cur.execute("SET GLOBAL net_buffer_length = 1000000;")
    cur.execute("SET GLOBAL max_allowed_packet = 1000000000;")
    db.commit()
    # The command is on for next connection.

    db = mysql.connector.connect(host="localhost", user="root", passwd="Listen", db="wikidata_simplified",\
        charset="utf8")
    cur = db.cursor()
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




init_mysql();

max_depth = 0

tree_assignment = []

def no_assignment(id, num):
	# print "******************"
	stack = [(id)]
	history = []
	idx = num
	global tree_assignment,max_depth
	depth = 0
	while len(stack):
		id = stack.pop()
		# print len(id)
		if len(id) > 1:
			depth -= 1
			tree_assignment.append((id[0],id[1],idx))
			idx += 1
			continue
		else:
			if id[0] in history:
				continue
			stack.append((id[0], idx))
			history.append(id[0])
			depth += 1
			# if depth > max_depth:
			# 	f = open("larry.txt","a")
			# 	f.write("%s %s\n" % (depth,id[0]))
			# 	max_depth = depth
			# 	f.close()
			idx = idx + 1

		sql = "select eid from Preced where weid = \"%s\"" % id
		cur.execute(sql)
		children = cur.fetchall()
		stack = stack + children
	
	return idx

def tree_build():
	global tree_assignment
	sql = "select eid from ancestor"
	cur.execute(sql)
	ancestor = cur.fetchall()
	print ancestor[1179]
	# print ancestor
	tree_sql = "insert ignore into htree (eid, lft, rgt) values (\"%s\",%s,%s)"
	num = 1
	a = 1
	for eid in ancestor:
		print "ancestor",a, max_depth, eid[0]
		a += 1

		tree_assignment = []
		num = no_assignment(eid,num)
		# print tree_assignment
		cur.executemany(tree_sql, tree_assignment)
		db.commit()
	
tree_build()


# def tree_search(eid):

# 	sql = "select weid from Preced where eid = \"%s\"" % eid
# 	cur.execute(sql)
# 	res = cur.fetchall()
# 	for weid in res:
# 		print weid[0]
# 		print "change tree"
# 		tree_search(weid[0])
# 		print "backward"

# def tree_search(eid):
# 	sql = "select lft,rgt from htree where eid = \"%s\"" % eid
# 	cur.execute(sql)
# 	res = cur.fetchall()
# 	print res
# 	sql = "select eid from htree where lft < 172800 and rgt > 172801"
# 	result = []
# 	# for lft,rgt in res:
# 	# 	print lft,rgt
# 	cur.execute(sql)
# 	result = result + cur.fetchall()
# 	return result


# start = time.time()
# print tree_search("Q18554966")
# print time.time() - start


