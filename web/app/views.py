# encoding=utf-8

from app import app
from flask import render_template, request, jsonify
# from models import Message
from datetime import datetime
# from src.NumberSequenceClassifier import number_clf
# import src.crf as CRF
# import src.rule as rule
import json

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/find_entity", methods=["POST"])
def find_entity():
    name = request.form.get("sent")
    # for s in sent.split("\n"):
        # print s
    # data = CRF.crf_tagger(sent)
    data = [
        ["P1", "HAH", "HAHA"]
    ]
    return jsonify(status='success',data=data)

@app.route("/find_tree", methods=["POST"])
def find_tree():
    eid = request.form.get("val")
    # for s in sent.split("\n"):
        # print s
    # data = CRF.crf_tagger(sent)
    data = [
        ["P1", "HAH", "HAHA"]
    ]
    return jsonify(status='success',data=data)

@app.route("/addDict", methods=["POST"])
def add_dict():
    dic = json.loads(request.form.get("dict"))
    print dic
    # status = rule.add_dict(dic)
    status = True
    return jsonify(status=status)

# @app.route("/message", methods=["POST"])
# def save_msg():
#     form = request.form
#     author = form.get("author")
#     content = form.get("content")
#     msg = Message(author=author, content=content, time=datetime.now())
#     msg.save()
#     return jsonify(status='success')


# @app.route("/messages")
# def list_msg():
#     page = request.args.get("page")
#     searchValue = request.args.get("searchValue")
#     if searchValue:
#         paginator =Message.objects(content__contains=searchValue).order_by('-time').paginate(page=int(page), per_page=5)
#     else:
#         paginator =Message.objects.order_by('-time').paginate(page=int(page), per_page=5)

#     pager = {
#         'page': paginator.page,
#         'pages': paginator.pages,
#         'messages': [m.to_json() for m in paginator.items]
#     }
#     return jsonify(status="success", pager=pager)


