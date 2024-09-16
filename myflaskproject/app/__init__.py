from flask import Flask

app = Flask(__name__)

# Import routes after initializing the app
from app import routes
