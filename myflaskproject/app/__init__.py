from flask import Flask

app = Flask(__name__)

# Import routes from the routes.py file
from app import routes
