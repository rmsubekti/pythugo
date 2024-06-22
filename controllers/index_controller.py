import sys
from flask import render_template, redirect, url_for, request, abort

from models.blog import Blog
from models.base import db
from controllers.auth_controller import login_required

def index():
    return render_template("index.html")