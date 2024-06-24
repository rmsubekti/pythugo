from flask import Blueprint

from controllers.blog_controller import create, index, show, editor, delete, getBlob, saveBlob

blog_bp = Blueprint('blog_bp', __name__)


blog_bp.route('/', methods=['GET'])(index)
blog_bp.route('/create', methods=['POST', "GET"])(create)
blog_bp.route('/<int:blog_id>/editor')(editor)
blog_bp.route('/<int:blog_id>/blob/<string:sha>')(getBlob)
blog_bp.route('/<int:blog_id>/blob/<string:sha>', methods=['POST'])(saveBlob)
blog_bp.route('/<int:blog_id>', methods=['DELETE'])(delete)
blog_bp.route('/<int:blog_id>', methods=['GET'])(show)
