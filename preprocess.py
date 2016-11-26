import json
import cPickle, os, sys
import MySQLdb

def init_mysql():
    global cur, db
    db = MySQLdb.connect(host="localhost", user="htl11", passwd="1234", db="Wikidata",\
        charset="utf8")
    cur = db.cursor()
    cur.execute("SET foreign_key_checks = 0")
    cur.execute("DELETE FROM entity")
    cur.execute("DELETE FROM datavalue")
    cur.execute("DELETE FROM time")
    cur.execute("DELETE FROM wikientityid")
    cur.execute("DELETE FROM quantity")
    cur.execute("DELETE FROM claim")
    # db.commit()
    cur.execute("INSERT IGNORE INTO item VALUES ('Q1'), ('Q2')")

init_mysql()
err_file = "err.log"
err_f = open(err_file, "w")


def insert_many(table, data_list, execute=True):
    if data_list == []:
        return
    data_list = data_list[:50]
    tpl = "%s," * len(data_list)
    print len(data_list[0]), data_list[0]
    if len(data_list[0]) == 1:
    # if isinstance(data_list[0], tuple):
        tpl = "(%s)," * len(data_list)
        for i, d in enumerate(data_list):
            data_list[i] = d[0]
    tpl = tpl[:-1]
    sql = "INSERT IGNORE INTO %s VALUES " % table
    sql += "{0}".format(tpl)
    try:
        if execute:
            return cur.execute(sql, data_list)
        else:
            return sql % tuple(data_list)
    except:
        print table
        print len(data_list)
        print data_list
        print sql
        print sql % tuple(data_list)
        err_f.write(table + "\n")
        raise
        # err_f.write("\n".join(data_list) + "\n\n")

def get_datavalue(valuetype, value):
    shortvalue = ""
    completevalue = []

    if isinstance(value, dict):
        for key, val in value.items():
            if not isinstance(val, unicode):
                value[key] = str(val).replace('"', '\\"').replace("'", "\\'")

    if valuetype == "string":
        shortvalue = value
        if isinstance(value, dict):
            shortvalue = value["value"]
        completevalue = (shortvalue, )
    elif valuetype == "wikibase-entityid":
        if value["entity-type"] == "item":
            shortvalue = "Q" + value["numeric-id"]
        elif value["entity-type"] == "property":
            shortvalue = "P" + value["numeric-id"]
        else:
            print value["entity-type"]
            raise ValueError("entity-type not eq to property or item!")
        completevalue = (shortvalue, )
        valuetype = "wikientityid"
    elif valuetype == "globecoordinate":
        shortvalue = "(%s, %s)" % (value["latitude"], value["longitude"])
        completevalue = tuple([value["latitude"], value["longitude"], \
            value["altitude"], value["precision"], value["globe"]])
    elif valuetype == "quantity":
        shortvalue = value["amount"]
        completevalue = tuple([value["amount"], value["upperBound"], \
            value["lowerBound"], value["unit"]])
    elif valuetype == "time":
        shortvalue = value["time"]
        completevalue = tuple([value["time"], value["timezone"], \
            value["before"], value["after"], value["precision"], \
            value["calendarmodel"]])
    elif valuetype == "monolingualtext":
        shortvalue = value["text"]
        completevalue = tuple([value["language"], value["text"]])
    else:
        print valuetype, value
        assert isinstance(value, str)
        shortvalue = value
        completevalue = (value, )
        valuetype = ""
        # raise ValueError("valuetype unknown!")

    return shortvalue, completevalue, valuetype

def commit_all(data_dict):
    for table, data_list in data_dict.items():
        print table
        insert_many(table, data_list, execute=True)


table_list = ["alias", "badge", "claim", "datavalue", "description", "entity", \
    "globecoordinate", "item", "label", "monolingualtext", "property", "qualifier", \
    "quantity", "reference", "referenceitem", "sitelink", "string", "time", "wikientityid"]
data_dict = {}
for table in table_list:
    data_dict[table] = []

def load_data(fname):
    f = open(fname, "r")
    
    line_cnt = 0

    cur.execute("SELECT did FROM Datavalue ORDER BY did DESC LIMIT 1")
    did = cur.fetchone()
    did = str(int(did[0]) if did is not None else -1)

    for line in f.xreadlines():
        line_cnt += 1
        # print line_cnt
        sys.stdout.flush()
        if line_cnt % 1000 == 0:
            commit_all(data_dict)
            for table in table_list:
                data_dict[table] = []
        line = line.strip()
        if line == "]" or line == "[":
            continue
        entity = json.loads(line[:-1])
        eid, pageid, ns, title, lastrevid, modified, _type = entity["id"], str(0), \
            str(0), "", str(0), "2015-02-27T14:37:20Z", entity["type"],
        entity_data = (eid, pageid, ns, lastrevid, modified, _type)
        data_dict["entity"].append(entity_data)
        if _type == "item":
            data_dict["item"].append((eid, ))
        else:
            data_dict["property"].append((eid, entity["datatype"]))
        try:
            alias_list = []
            for aliases in entity["aliases"].values():
                for alias in aliases:
                    alias_list.append((eid, alias["language"], alias["value"]))
            data_dict["alias"] += alias_list
      

            label_list = []
            for label in entity["labels"].values():
                label_list.append((eid, label["language"], label["value"]))
            data_dict["label"] += label_list

            desc_list = []
            for desc in entity["descriptions"].values():
                desc_list.append((eid, desc["language"], desc["value"]))
            data_dict["description"] += desc_list

 
            # print "lastdid", did
            datavalue_list = []
            claim_list = []
            qualifier_list = []
            ref_list = []
            ref_item_list = []
            for claims in entity["claims"].values():
                for claim in claims:
                    did = str(int(did) + 1)
                    cid, _type, rank = claim["id"], claim["type"], claim["rank"]
                    rank = str(2 if rank == "deprecated" else 1 if rank == "normal" else 2)
                    mainsnak = claim["mainsnak"]
                    snaktype, pid, datatype = mainsnak["snaktype"], mainsnak["property"], \
                        mainsnak["datatype"]
                    value = ""
                    if "datavalue" in mainsnak:
                        valuetype = mainsnak["datavalue"]["type"]
                        value = mainsnak["datavalue"]["value"]
                        shortvalue, completevalue, valuetable = get_datavalue(valuetype, value)
                        completevalue = (did, ) + completevalue
                        data_dict[valuetable].append(completevalue)
                        datavalue_list.append((did, valuetype)) 

                    claim_list.append((cid, _type, snaktype, pid, rank, datatype, \
                        valuetype, shortvalue, did))

                    if "qualifiers" in claim:                
                        qualifier_order = {}
                        # print claim
                        for i, pid in enumerate(claim["qualifiers-order"]):
                            qualifier_order[pid] = str(i)
                        for qualifiers in claim["qualifiers"].values():
                            for qua in qualifiers:
                                did = str(int(did) + 1)
                                # print qua
                                qid, qsnaktype, qpid, qdatatype = qua["hash"], \
                                    qua["snaktype"], qua["property"], qua["datatype"]
                                qrank = qualifier_order[qpid]
                                qvaluetype = ""
                                qvalue = ""
                                if "datavalue" in qua:
                                    qvalue = qua["datavalue"]
                                    qvaluetype = qvalue["type"]
                                    qvalue = qvalue["value"]
                                    qshortvalue, qcompletevalue, qvaluetable = get_datavalue(qvaluetype, qvalue)
                                    qcompletevalue = (did,) + qcompletevalue
                                    data_dict[qvaluetable].append(qcompletevalue)
                                    datavalue_list.append((did, qvaluetype))
                                qualifier_list.append((qid, cid, qsnaktype, qpid, qrank, qdatatype,\
                                    qvaluetype, qshortvalue, did))

                    if "references" in claim:
                        for ref in claim["references"]:
                            ref_order = {}
                            for i, pid in enumerate(ref["snaks-order"]):
                                ref_order[pid] = str(i)
                            rid = ref["hash"]
                            # print rid, eid
                            ref_list.append((rid, cid))
                            for snaks in ref["snaks"].values():
                                for snak in snaks:
                                    did = str(int(did) + 1)
                                    rsnaktype, rpid, rdatatype = snak["snaktype"], snak["property"],\
                                        snak["datatype"]
                                    rrank = ref_order[rpid]
                                    rvalue = ""
                                    rvaluetype = ""
                                    if "datavalue" in snak:
                                        rvalue = snak["datavalue"]
                                        rvaluetype = rvalue["type"]
                                        rvalue = rvalue["value"]
                                        rshortvalue, rcompletevalue, rvaluetable = get_datavalue(rvaluetype, rvalue)
                                        rcompletevalue = (did,) + rcompletevalue
                                        data_dict[rvaluetable].append(rcompletevalue)
                                        datavalue_list.append((did, rvaluetype))
                                    ref_item_list.append((rid, rsnaktype, rpid, rrank, rdatatype, \
                                        rvaluetype, rshortvalue, did))

            data_dict["datavalue"] += datavalue_list
            data_dict["claim"] += claim_list
            data_dict["qualifier"] += qualifier_list
            data_dict["reference"] += ref_list
            data_dict["referenceitem"] += ref_item_list

        except:
            # for i in label_list:
            #     print len(i[1]), len(i[2])
            # print sql
            raise


        # db.commit()
        # break
    print line_cnt
    f.close()
    pass

def main():
    load_data("C:/Users/t-honlin/Desktop/wikidata.json")
    pass

if __name__ == '__main__':
    main()
    db.close()
    pass