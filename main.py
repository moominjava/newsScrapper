import requests
from flask import Flask, render_template, request


base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api


db = {}
app = Flask("DayNine")

def news_data():
  new_datas = "new"
  getDb = db.get(f"news:{new_datas}")
  if getDb:
    news = getDb
  else:
    news = new_list()
    db[f"news:{new_datas}"] = news
  return news

def popular_data():
  popular_datas = "popular"
  getDb = db.get(f"news:{popular_datas}")
  if getDb:
    news = getDb
  else:
    news = popular_list()
    db[f"news:{popular_datas}"] = news
  return news


def new_list():
  new_datas = []
  new_result = requests.get(new)
  new_results = new_result.json()
  new_dict = new_results['hits']
  for item in new_dict:
    new_datas.append(item)
  return new_datas

def popular_list():
  popular_datas = []
  popular_result = requests.get(popular)
  popular_results = popular_result.json()
  popular_dict = popular_results['hits']
  for item in popular_dict:
    popular_datas.append(item)
  return popular_datas

def make_detail_url(id):
  return f"{base_url}/items/{id}"


@app.route("/")
def home():
  #url = None
  if request.args.get("order_by", "") == "":
    url = None
  else:
    url = request.args.get("order_by", "")
  if url == "popular" or url == None:
    news = popular_data()
  else:
    news = news_data()
  return render_template("index.html", news = news, url = url)
  
@app.route("/<id>")
def detail(id ):
  detail_url = make_detail_url(id)
  detail_data = requests.get(detail_url)
  detail_news = detail_data.json()
  children = []
  children_data = detail_news['children']
  for child in children_data:
    children.append(child)
  return render_template(
    "detail.html",
    children = children,
    detail_news = detail_news
    )

app.run(host="0.0.0.0")

