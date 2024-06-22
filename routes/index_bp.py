from flask import Blueprint

from controllers.index_controller import *

index_bp = Blueprint('index_bp', __name__)

index_bp.route('/')(index)