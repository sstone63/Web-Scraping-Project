from flask import Flask, render_template, redirect
import mars_scrape 
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_database
collection = db.mars_database

@app.route("/")
def home():
    scrape_dict = collection.find_one()

    return render_template("index.html", dict=scrape_dict)

@app.route("/scrape")
def scrape_mars():
    mars_dict = mars_scrape.scrape()

    collection.update({}, {"$set": mars_dict}, upsert=True)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
