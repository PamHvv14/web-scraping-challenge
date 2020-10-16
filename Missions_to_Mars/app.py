from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

app.config[...] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def ...():


    return render_template("index.html", ...