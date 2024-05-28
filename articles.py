from flask import Flask, request, abort, jsonify, render_template, make_response, redirect
from subprocess import run
import requests
import uuid
import mariadb

app = Flask(__name__)

run(['docker-compose', f'-fmaria.yml', 'up', '-d'])

def get_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="123",
            host="127.0.0.1",
            port=3306,
            database="articles"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    return conn

@app.route("/", methods=["POST", "GET"])
def handle_index():
    return redirect("http://127.0.0.1:8000/", code=302)

@app.route("/login", methods=["POST", "GET"])
def handle_login():
    return redirect("http://127.0.0.1:8001/login", code=302)

@app.route("/articles", methods=["POST", "GET"])
def handle_articles():
    data = []
    cur = get_connection().cursor()
    cur.execute("SELECT * FROM articles_tbl")
    all = cur.fetchall()
    for article in all:
        data.append({'article_name':article[1],
                     'article_text': article[2], 
                     'article_author':article[3], 
                     'article_date': article[4]})
    #print(all)
    if request.method == "POST":
        resp = make_response(render_template('articles.html', articles=data))
        return resp, 200
    elif request.method == "GET":
        resp = make_response(render_template('articles.html', articles=data))
        return resp, 200
    else:
        abort(400)

@app.route("/adopt", methods=["POST", "GET"])
def handle_adopt():
    return redirect("http://127.0.0.1:8003/adopt", code=302)

@app.route("/help", methods=["POST", "GET"])
def handle_help():
    return redirect("http://127.0.0.1:8004/help", code=302)

@app.route("/create_article", methods=["POST", "GET"])
def handle_generator():
    return redirect("http://127.0.0.1:8010/create_article", code=302)

if __name__ == "__main__":
    app.run(port=8002)

try:
    while True:
        pass
except KeyboardInterrupt:
    run(['docker-compose', f'-fmaria.yml', 'stop'])