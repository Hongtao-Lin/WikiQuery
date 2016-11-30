import json
import cPickle, os, sys, time
import mysql.connector

def init_mysql(dbname):
    global cur, db
    # First extend the max_packet size.
    db = mysql.connector.connect(host="localhost", user="root", passwd="Listen", db=dbname,\
        charset="utf8")
    cur = db.cursor()
    cur.execute("SET GLOBAL net_buffer_length = %s" % 1000000)
    cur.execute("SET GLOBAL max_allowed_packet = 1000000000")
    db.commit()
    # The command is on for next connection.
    db = mysql.connector.connect(host="localhost", user="root", passwd="Listen", db=dbname,\
        charset="utf8")
    # cur.execute("SET character_set_client  = utf8mb4")
    # cur.execute("SET character_set_results = utf8mb4")
    # cur.execute("SET collation_connection  = utf8mb4_general_ci")
    cur = db.cursor()
    cur.execute("SET foreign_key_checks = 0")
    # cur.execute("INSERT INTO item VALUES ('P1');")
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

# INIT
dbname = "wikidata_simplified2"
init_mysql(dbname)
prop_dict = get_valid_properties("./properties.txt")
tables = ["alias", "badge", "claim", "datavalue", "description", "entity", \
    "globecoordinate", "item", "label", "monolingualtext", "property", "qualifier", \
    "quantity", "reference", "referenceitem", "sitelink", "string", "time", "wikientityid", "cqmapping", "correlation", "preced"]
data_dict = {}
for table in tables:
    data_dict[table] = []

# filter_pid (bool): If true, filter the property according the extracted list.
# ignore_datavalue (bool): If true, do not insert specific datavalue into specific tables.
# combine_qua_claim (bool): If true, add qualifier-hash as a field in claim.
#   It may require more space, but time-efficient in querying qualifier.
#   We also simplified the schema of claim.
ignore_datavalue = True
filter_pid = True
combine_qua_claim = True
# Acutal table used: entity, item, property, claim
ignored_tables = ["badge", "reference",\
    "referenceitem", "sitelink"]
datavalue_tables = ["datavalue", "globecoordinate","monolingualtext", "quantity",\
    "string", "time", "wikientityid"]
if ignore_datavalue:
    ignored_tables += datavalue_tables
    did = '-1'
else:
    cur.execute("SELECT did FROM Datavalue ORDER BY did DESC LIMIT 1")
    # Data id for increment in datavalue.
    did = cur.fetchone()
    did = str(int(did[0]) if did is not None else -1)

def insert_many(table, data_list, max_num=-1, execute=True):
    """For efficiency.
    
    Args:
        table (str): name of table to be inserted
        data_list (list): a list of *tuple*.
        max_num (int, optional): If > 0, only insert the first k entries.
        execute (bool, optional): only execute if it's true.
    
    Returns:
        If execute = True, return status of execution.
        else: return the sql.
    """
    if data_list == []:
        return
    if table in ignored_tables:
        return
    if max_num == -1:
        max_num = len(data_list)
    data_list = data_list[:max_num]

    tpl = "%s," * len(data_list[0])
    tpl = tpl[:-1]
    # sql = "INSERT IGNORE INTO %s VALUES " % table.capitalize()
    sql = "INSERT IGNORE INTO %s VALUES " % table.capitalize()
    sql += "({0})".format(tpl)
    try:
        if execute:
            return cur.executemany(sql, data_list)
        else:
            return sql % tuple(data_list)
    except:
        print table
        print len(data_list)
        # print data_list
        print sql
        # print sql % tuple(data_list)
        raise

def commit_all(data_dict):
    # print data_dict["claim"][0]
    for table, data_list in data_dict.items():
        # print table
        insert_many(table, data_list, max_num=-1, execute=True)
    db.commit()

    for table in tables:
        data_dict[table] = []

def get_datavalue(valuetype, value):
    """Get different value strucutures according to its type.
    Note that some of the value is a single string!
    Returns:
        shortvalue (str): the concatenated value for display.
        completevalue (tuple): the whole value extracted from structure.
        valuetable (str): the corresponding table to insert.
    """
    shortvalue = ""
    completevalue = []
    valuetable = valuetype

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
        valuetable = "wikientityid"
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
        valuetable = ""
        # raise ValueError("valuetype unknown!")

    return shortvalue, completevalue, valuetable

def get_and_store_snak_datavalue(snak, datavalue_list):
    valuetype = snak["datavalue"]["type"]
    value = snak["datavalue"]["value"]
    shortvalue, completevalue, valuetable = get_datavalue(valuetype, value)
    tmp_did = did
    if ignore_datavalue:
        tmp_did = None
    completevalue = (tmp_did, ) + completevalue
    data_dict[valuetable].append(completevalue)
    datavalue_list.append((did, valuetype))
    return shortvalue, valuetype

def load_data(fname, skip=0):
    """Load the whole data from json.
    First parse each line of json, 
    Then collect tuples of data into *data_dict*
    Then commit the whole data_dict as a whole for efficiency.
    """
    global did
    f = open(fname, "r")
    print "in"
    line_cnt = 0
    start = time.time()

    for line in f.xreadlines():
        line_cnt += 1
        line = line.strip()
        if line == "]" or line == "[":
            continue
        if line_cnt <= skip:
            if line_cnt % 10000 == 0:
                print "Skipped", line_cnt
            continue
        entity = json.loads(line[:-1])
        eid, etype = entity["id"], entity["type"]
        en_desc, en_label = "", ""

        if etype == "property" and eid not in prop_dict:
            continue

        if etype == "item":
            data_dict["item"].append((eid, ))
        else:
            data_dict["property"].append((eid, entity["datatype"]))

        alias_list = []
        for aliases in entity["aliases"].values():
            for alias in aliases:
                lang, val = alias["language"], alias["value"]
                if lang not in ["en", "zh-hans"]:
                    continue
                alias_list.append((eid, lang, val))
        data_dict["alias"] += alias_list
  

        label_list = []
        for label in entity["labels"].values():
            lang, val = label["language"], label["value"]
            if lang not in ["en", "zh-hans"]:
                continue
            label_list.append((eid, lang, val))
            if lang == "en":
                en_label = val
        data_dict["label"] += label_list

        desc_list = []
        for desc in entity["descriptions"].values():
            lang, val = desc["language"], desc["value"]
            if lang not in ["en", "zh-hans"]:
                continue
            desc_list.append((eid, lang, val))
            if lang == "en":
                en_desc = val
        data_dict["description"] += desc_list

        if etype == "item":
            sitelink_list = []
            badge_list = []
            for sitelink in entity["sitelinks"].values():
                site, title = sitelink["site"], sitelink["title"]
                sitelink_list.append((eid, site, title))
                for badge in sitelink["badges"]:
                    badge_list.append((site, title, badge))
            data_dict["sitelink"] += sitelink_list
            data_dict["badge"] += badge_list

        entity_data = (eid, en_label, en_desc, etype)
        data_dict["entity"].append(entity_data)

        datavalue_list = []
        claim_list = []
        qualifier_list = []
        ref_list = []
        ref_item_list = []
        cqmapping_list = []
        preced_list = []
        correlation_list = []
        for claims in entity["claims"].values():
            for claim in claims:
                cid, _type, rank = claim["id"], claim["type"], claim["rank"]
                rank = str(2 if rank == "deprecated" else 1 if rank == "normal" else 2)
                mainsnak = claim["mainsnak"]
                snaktype, pid, datatype = mainsnak["snaktype"], mainsnak["property"], \
                    mainsnak["datatype"]
                if filter_pid and (pid not in prop_dict):
                    continue
                did = str(int(did) + 1)
                shortvalue, valuetype = "", ""
                if "datavalue" in mainsnak:
                    shortvalue, valuetype = get_and_store_snak_datavalue(mainsnak, \
                        datavalue_list)
                    if "wikibase-entityid" == valuetype:
                        correlation_list.append((eid, shortvalue, cid))
                        if pid == "P279" or pid == "P31":
                            preced_list.append((eid,shortvalue))

                if not combine_qua_claim:
                    claim_list.append((cid, eid, en_label, _type, snaktype, pid, prop_dict[pid],\
                        rank, datatype, valuetype, shortvalue, did))
                else:
                    claim_list.append((cid, eid, pid, shortvalue))
                # if etype == "item":
                #     print eid, claim_list[-1]
                if "qualifiers" in claim:
                    qualifier_order = {}
                    # print claim
                    for i, pid in enumerate(claim["qualifiers-order"]):
                        qualifier_order[pid] = str(i)
                    for qualifiers in claim["qualifiers"].values():
                        for qua in qualifiers:
                            # print qua
                            qid, qsnaktype, qpid, qdatatype = qua["hash"], \
                                qua["snaktype"], qua["property"], qua["datatype"]
                            if filter_pid and (qpid not in prop_dict):
                                continue
                            did = str(int(did) + 1)
                            qrank = qualifier_order[qpid]
                            qvaluetype = ""
                            qshortvalue = ""
                            if "datavalue" in qua:
                                qshortvalue, qvaluetype = get_and_store_snak_datavalue(qua, \
                                    datavalue_list)
                                if "wikibase-entityid" == qvaluetype:
                                    correlation_list.append((eid, qshortvalue, cid));

                            if combine_qua_claim:
                                cqmapping_list.append((cid,qid))
                                qualifier_list.append((qid, qpid, qshortvalue))
                            else:
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
                                rsnaktype, rpid, rdatatype = snak["snaktype"], snak["property"],\
                                    snak["datatype"]
                                if filter_pid and (rpid not in prop_dict):
                                    continue
                                did = str(int(did) + 1)
                                rrank = ref_order[rpid]
                                rvaluetype = ""
                                rshortvalue = ""
                                if "datavalue" in snak:
                                    rshortvalue, rvaluetype = get_and_store_snak_datavalue(snak, \
                                        datavalue_list)
                                ref_item_list.append((rid, rsnaktype, rpid, rrank, rdatatype, \
                                    rvaluetype, rshortvalue, did))

        data_dict["datavalue"] += datavalue_list
        data_dict["claim"] += claim_list
        data_dict["qualifier"] += qualifier_list
        data_dict["reference"] += ref_list
        data_dict["referenceitem"] += ref_item_list
        data_dict["correlation"] += correlation_list
        data_dict["preced"] += preced_list
        data_dict["cqmapping"] += cqmapping_list

        if line_cnt % 10000 == 0:
            sys.stdout.flush()
            commit_all(data_dict)
            print line_cnt, time.time() - start
            start = time.time()
            

    print line_cnt
    f.close()
    pass

def get_all_properties(fname, oname):
    f = open(fname)
    o = open(oname, "w")
    for line in f.readlines():
        line = line.decode("utf8").strip().split("\t")
        print line
        if line == []:
            continue
        pid = line[0].split()[-1][1:-1]
        pval = " ".join(line[0].split()[:-1])
        pval = pval.lower()
        info = "\t".join([pid, pval])
        o.write(info.encode("utf8") + "\n")
    f.close()
    o.close()

def main():
    start = time.time()
    # get_all_properties("C:/Users/t-honlin/Desktop/properties.txt", "./properties.txt")
    load_data("/home/larryeye/WikiQuery/wikidata.json", skip=0)
    print time.time() - start
    pass

if __name__ == '__main__':
    main()
    db.close()
    pass