# import necessary libraries
from flask import Flask, render_template, redirect, url_for 
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

#flask pymongo to set up the connection to de data base
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.marsData.find_one()
   # print(mars_data)
    #return mars_data
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    # reference data collection
    marsTable = mongo.db.marsData

    #drop the table
    mongo.db.marsData.drop()

    #c call scrape mars script
    mars_data = scrape_mars.scrape_all()

    # take a dictionary and load into Mondosdb 
    marsTable.insert_one(mars_data)

    #print(mars_data) #Print the dictionary scrape_mars.py
    # back to the index
    return redirect("/")

# Set up a flask app
if __name__ == "__main__":
    app.run(port=8000)