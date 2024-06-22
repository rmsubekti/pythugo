import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
#docker run --name pythugo -e MYSQL_USER=pythugo -e MYSQL_PASSWORD=pythugo -e MYSQL_DATABASE=pythugo -e MYSQL_ROOT_PASSWORD=pythugo -p 33060:33060 -d mysql
SQLALCHEMY_DATABASE_URI=os.getenv("MYSQL_URI")

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ENV
GITHUB_CLIENT_ID=os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET=os.getenv("GITHUB_CLIENT_SECRET")