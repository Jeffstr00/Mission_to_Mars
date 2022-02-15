# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up route for main HTML page
#tells Flask what to display when looking at homepage
@app.route("/")
def index():
    # uses PyMongo to find the "mars" collection in our database
    mars = mongo.db.mars.find_one()
    # tells Flask to return an HTML template using an index.html file
    # "mars=mars" tells Python to use the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)

# set up scraping route
# defines the route that Flask will be using; the route "/scrape" will run the function below
@app.route("/scrape")
def scrape():
    # assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # create a new variable to hold the newly scraped data, referencing the "scrape_all" function in the scraping.py file exported from Jupyter Notebook
    mars_data = scraping.scrape_all()
    # update database using .update_one(), but not if an identical record already exists
    # {"$set": data} means that the document will be modified ("$set") with the data in question.
    # upsert=True tells Mongo to create new document if one doesn't already exist, and new data will always be saved
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    # after scraping data, navigate back to / to see updated content
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()