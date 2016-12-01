# encoding=utf-8

from app import app
from flask import render_template, request, jsonify
# from models import Message
from datetime import datetime
import requests
# from src.NumberSequenceClassifier import number_clf
# import src.crf as CRF
# import src.rule as rule
import json

# Helper func:
def load_property(fname):
    f = open(fname)
    prop_dict = {}
    for line in f.xreadlines():
        pid, pname = line.decode("utf8").strip().split("\t")
        prop_dict[pname] = pid
    f.close()
    return prop_dict
pfname = "../properties.txt"
prop_dict = load_property(pfname)

def find_tree(eid):
    data = [
        ["P1", "HAH", "HAHA"]
    ]
    return data

def find_relation(eid):
    data = [
        ["P1", "HAH", "HAHA"]
    ]
    return data

def find_cooccur(eid):
    data = [
        ["P1", "HAH", "HAHA"]
    ]
    return data

def find_entityid(ename):
    """Take the first one if many applies
    Prompt: return the error message ready to show in front-end.
    """
    eid = "Q1"
    prompt = ""
    return eid, prompt


def find_aliasid(ename):
    """Take the first one if many applies"""
    eid = "Q1"
    prompt = ""
    return eid, prompt

def find_value(eid):
    value = "ha"
    prompt = ""
    return value, prompt

def find_description(eid):
    desc = "desc"
    prompt = ""
    return desc, prompt

def find_claim(eid, pid):
    """Prompt return "is_entity" if the corresponding value is entity!"""
    claim = "claim"
    prompt = ""
    return claim, prompt

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nlq")
def nlq():
    return render_template("nlq.html")

@app.route("/nlq_ask", methods=["POST"])
# Note: prompt is the specific error message to display in final answer.
def nlq_ask():
    args = request.form.get("args")
    args = json.loads(args)
    prompt = ""
    answer = ""
    item = args.get("item", "")
    prop = args.get("property", "")
    if not item:
        prompt = "Cannot find the entity you mentioned!"

    # get eid of the item according to its name or alias.
    eid, prompt = find_entityid(item)
    if prompt:  
        eid, prompt = find_aliasid(item)
    if eid:
        # if no property detected, we consider it as to find a description 
        if not prop:
            answer, prompt = find_description(eid)
        else:
            pid = prop_dict[prop]   # get pid according to dict.
            # find the value in claim triple, the prompt maybe error msg, "is_entity" or ""
            answer, prompt = find_claim(eid, pid)
            if prompt == "is_entity":
                # if the answer is a eid, find its value.
                answer, prompt = find_value(answer)


    answer = "Just a test"
    if prompt:
        return jsonify(status='fail',data=prompt)
    return jsonify(status='success',data=answer)


@app.route("/find_entity", methods=["POST"])
def find_entity():
    name = request.form.get("sent")
    # for s in sent.split("\n"):
        # print s
    # data = CRF.crf_tagger(sent)
    data = [
        ["P1", "HAH", "HAHA"],
        ["P2", "HAH", "HAHA"],
    ]
    return jsonify(status='success',data=data)

@app.route("/secondary_query", methods=["POST"])
def secondary_query():
    eid = request.form.get("eid")
    qtype = request.form.get("qtype")

    data = [
        ["P1", "HAH", "HAHA"]
    ]
    if qtype == 1:
        data = find_tree(eid)
    elif qtype == 2:
        data = find_relation(eid)
    elif qtype == 3:    
        data = find_cooccur(eid)

    # for s in sent.split("\n"):
        # print s
    # data = CRF.crf_tagger(sent)
    return jsonify(status='success',data=data)

@app.route("/addDict", methods=["POST"])
def add_dict():
    dic = json.loads(request.form.get("dict"))
    print dic
    # status = rule.add_dict(dic)
    status = True
    return jsonify(status=status)