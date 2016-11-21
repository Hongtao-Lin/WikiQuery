import json
import cPickle
import MySQLdb

def init_mysql():
    global cur, db
    db = MySQLdb.connect(host="localhost", user="htl11", passwd="1234", db="Wikidata",\
        charset="utf8")
    cur = db.cursor()
    cur.execute("DELETE FROM entity")
    cur.execute("SET foreign_key_checks = 0")
    db.commit()
    # cur.execute("SELECT * FROM entity")
    # print cur.fetchall()

init_mysql()

def load_data(fname):
    f = open(fname, "r")
    for line in f.xreadlines():
        line = line.strip()
        if line == "]" or line == "[":
            continue
        entity = json.loads(line[:-1])
        eid, pageid, ns, title, lastrevid, modified, _type = entity["id"], int(0), \
            int(0), "", int(0), "2015-02-27T14:37:20Z", entity["type"],
        # assert eid == title
        # cur.execute('''INSERT INTO entity VALUES (%s, %s, %s, %s, %s, %s)''', \
        #     (eid, pageid, ns, lastrevid, modified, _type))
        # db.commit()
        try:
            alias_list = []
            for aliases in entity["aliases"].values():
                for alias in aliases:
                    alias_list.append((eid, alias["language"], alias["value"]))
            alias_list = alias_list[:1]
            alias_tpl = ",".join(['%s'] * len(alias_list))
            sql = "INSERT INTO alias VALUES {0}".format(alias_tpl)
            cur.execute(sql, alias_list)        

            label_list = []
            for label in entity["labels"].values():
                label_list.append((eid, label["language"], label["value"]))
            label_list = label_list[:40]
            label_tpl = ",".join(['%s'] * len(label_list))
            sql = "INSERT INTO label VALUES {0}".format(label_tpl)
            cur.execute(sql, label_list)  

            desc_list = []
            for desc in entity["description"].values():
                desc_list.append((eid, desc["language"], desc["value"]))

            desc_tpl = ",".join(['%s'] * len(desc_list))
            sql = "INSERT INTO description VALUES {0}".format(desc_tpl)
            cur.execute(sql, desc_list)  
        except:
            for i in label_list:
                print len(i[1]), len(i[2])
            print sql
            raise


        db.commit()
        break
    f.close()
    pass

def main():
    load_data("C:/Users/t-honlin/Desktop/wikidata.json")
    pass

if __name__ == '__main__':
    main()
    db.close()
    pass