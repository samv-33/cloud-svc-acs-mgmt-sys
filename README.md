# cloud-svc-acs-mgmt-sys

# Team Members

Samuel Vo
Jacob Corletto
Angel Fuentes

# Instructions to Install and Run

Instructions how to run the program:
Prerequisites Python 3.7+ - Download from Python's official website.
MongoDB Compass -

pip - Should come installed with Python; if not, install it using:

python -m ensurepip --upgrade

run pip --version to check if it is the latest one.

Steps to Set Up

Clone the Repository git clone:

Create and Activate a Virtual Environment It’s recommended to run this project in a virtual environment to manage dependencies.
Create a virtual environment
python -m venv venv

Activate the virtual environment:

venv\Scripts\activate

## Install all dependencies by doing:

pip install -r requirements.txt

## Running the server

type:
uvicorn services:app --reload
into the terminal to run the server

# Instructions to setup Database with MongoDB Compass

Download latest version of MongoDB Compass or MongoDB shell from the official website

Create a new Connection, and name it anything you like:

I named mine "cloud_access_management"

Create a Database, we used "my_database" for the name. I would recommend using this name
to be consistent with the configurations on our models.py file

Also create each collection accordingly to our collection names in models.py for efficiency
So like (users_collection, )

# Instructions to setup Database with MongoDB Atlas

create a new ".env" file

Log into MongoDB and create a new cluster

add your URL given into your .env file as "MONGO_URI"

# Testing

with the server running in one terminal, navigate to localhost:8000/docs to test using swagger
