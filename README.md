# cloud-svc-acs-mgmt-sys

# Team Members

CPSC 449-03
Samuel Vo
Jacob Corletto
Angel Fuentes

# Video Part 1 and Part 2
https://drive.google.com/file/d/1vkpjqxO9-aXJKBwaAL78v2bZ3z8Zjh4G/view?usp=sharing - pt. 1

https://drive.google.com/file/d/19Y1pZBiXxjLTN6x8la5cih-FeP-OUcO8/view?usp=sharing - pt. 2


# Instructions to Install and Run

Instructions how to run the program:
Prerequisites Python 3.7+ - Download from Python's official website.
MongoDB Compass, MongoDB Shell, or Atlas could be used. 

pip - Should come installed with Python; if not, install it using:

python -m ensurepip --upgrade

run pip --version to check if it is the latest one.

# Steps to Set Up

Clone the Repository git clone:

 https://github.com/samv-33/cloud-svc-acs-mgmt-sys.git

Create and Activate a Virtual Environment It’s recommended to run 
this project in a virtual environment to manage dependencies.
Create a virtual environment:

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
So like (users_collection, sub_plan_collection, etc.)

We used an .env file, so you could just rename ".env.sample" to .env and use the db information
provided. Unless the localhost url is different then you could change it to the localhost url provided
by your database settings in Mongodb. 

MongoDB Compass should provide the local mongo url.

# Instructions to setup Database with MongoDB Atlas

create a new ".env" file

Log into MongoDB and create a new cluster

add your URL given into your .env file as "MONGO_URI"

# Testing

with the server running in one terminal, navigate to localhost:8000/docs to test using swagger

Or Log into Postman if you would like to test it there as well:

# POSTMAN INSTRUCTIONS:
1. Base URL
Make sure your FastAPI server is running. By default, it should be accessible at:
http://127.0.0.1:8000/
All the Object IDs and other IDs will be in the Database available to copy and paste
for reuse on each API endpoint.

2. General Steps
Open Postman and create a new request.
Set the request method (GET, POST, PUT, DELETE) and the URL for the endpoint.
Add required headers, body, and parameters as described below for each endpoint.
Click Send to execute the request.
Review the response in Postman.

Endpoints Instructions

1. Create Subscription Plan
Endpoint: POST /plans
Method: POST
Headers:
Content-Type: application/json
Body (JSON):

API POST /plans Create Plan
Input information in a form like this in the request body:
{
  "name": "Master Plan",
  "description": "Premium with unlimited access to an API plus admin role.",
  "api_permissions": ["read", "write", "admin"],
  "usage_limits": {"daily": 2000, "monthly": 5000}
}
It should return with the plan created


2. Update Subscription Plan

Endpoint: PUT /plans/{plan_id}
Method: PUT
Headers:
Content-Type: application/json
Path Parameters:
plan_id: Replace {plan_id} with the MongoDB ObjectId of the plan to update.
You can find this in the database for sub_plan_collection.
Body (JSON):
json
The format should be like this:
{
  "name": "Middle Plan",
  "description": "Simple plan with limited access.",
  "api_permissions": ["read", "write"],
  "usage_limits": {"daily": 1000, "monthly": 2000}
}
It should update the plan.

3. Delete Subscription Plan
Endpoint: DELETE /plans/{plan_id}
Method: DELETE
Path Parameters:
plan_id: Replace {plan_id} with the MongoDB ObjectId of the plan to delete.
It should show a message that the plan was deleted.

4. Add Permission
Endpoint: POST /permissions
Method: POST
Headers:
Content-Type: application/json
Body (JSON):
Follow this format to input into the Request Body:
{
  "name": "Write Permission",
  "description": "Grants write access.",
  "api_endpoint": "/api/v1/write"
}
It should show a message that you created the plan.


5. Update Permission
Endpoint: PUT /permissions/{permission_id}
Method: PUT
Headers:
Content-Type: application/json
Path Parameters:
permission_id: Replace {permission_id} with the MongoDB ObjectId of the permission to update.
Body (JSON):
Using the same format, modify the contents:
{
  "name": "Create Permission",
  "description": "Grants create access.",
  "api_endpoint": "/api/v1/create"
}
It should return a message that the permission is updated.

6. Delete Permission
Endpoint: DELETE /permissions/{permission_id}
Method: DELETE
Path Parameters:
permission_id: Replace {permission_id} with the MongoDB ObjectId of the permission to delete.
There will be a message showing permission deleted!

7. Create User
Endpoint: POST /users
Method: POST
Headers:
Content-Type: application/json
Body (JSON):
Follow this format:
{
    "username": "Bob Mailman",
    "email": "Bob@email.com"
}
The new user should be created and there should be a message.


8. Get User
Endpoint: GET /users/{user_id}
Method: GET
Path Parameters:
user_id: Replace {user_id} with the MongoDB ObjectId of the user in the url.

9. Create Subscription
Endpoint: POST /subscriptions
Method: POST
Headers:
Content-Type: application/json
Body (JSON):
Follow this format in the request body:
{
    "user_id": "6762509f4531b9a2352ff2f4",
    "plan_id": "675e528521e07e7a5d7d7e1f",
    "start_date": "2024-12-15T12:09:00+00:00",
    "end_date": "2024-12-15T12:11:00+00:00"
}
It should show a message that a new subscription is created.

10. Get Subscriptions for User
Endpoint: GET /subscriptions/{user_id}
Method: GET
Path Parameters:
user_id: Replace {user_id} with the MongoDB ObjectId of the user.

11. Track Usage
Endpoint: POST /usage
Method: POST
Headers:
Content-Type: application/json
Body (JSON):
json
Format it like this in the request body:
{
  "user_id": "6762509f4531b9a2352ff2f4",
  "api_endpoint": "/read",
  "api_calls": 65,
  "storage_used": 100
}
It should give a message like user tracked. 

12. Get Usage Stats
Endpoint: GET /subscriptions/{user_id}/usage
Method: GET
Path Parameters:
user_id: Replace {user_id} with the MongoDB ObjectId of the user.
It should get information about usage statistics from the user. 

13. Assign/Modify User Plan
Endpoint: PUT /subscriptions/{user_id}
Method: PUT
Enter the URL: Replace {user_id} with the actual user ID of the user whose subscription you want to update.
Add Query Parameters
Add the following query parameter:
Key: plan_id (write it exactly in the Query parameters)
Value: The ID of the subscription plan you want to assign to the user.
It will print a message about the user's subscription plan has been updated. 
You could view this in the subscriptions_collection in the database. 

14. Check Access
Endpoint: GET /access/{user_id}/{api_endpoint}
Method: GET
Path Parameters:
user_id: Replace {user_id} with the MongoDB ObjectId of the user.
api_endpoint: Replace {api_endpoint} with the endpoint you want to check access for.
If it is the correct api_endpoint within the scope of your subscription plan then
it will show a message access granted. 


15. Track API Request
Endpoint: POST /usage/{user_id}
Method: POST
Enter the URL: Replace {user_id} in the URL with the actual user ID.
Enter in Query Parameters:
Key: api_endpoint (click the checkmark), Value: endpoint (any api_endpoint you want)
URL path should look like this:  {user_id}/?api_endpoint=endpoint (any api_endpoint you want to be tracked)
It should give you a message that the api is being tracked and it should appear in the 
usage_collection. 

16. Check Usage Limit
Endpoint: GET /usage/{user_id}/limit
Method: GET
Enter the URL: Replace {user_id} with the actual user ID and include the api_endpoint as a query parameter.
Example:
Add Query Parameters information: 
Key: api_endpoint (add this exact key just like previous endpoint)
Value: read (example endpoint)
It should give a message about the limit status of the api_endpoint used from that specific user. 
