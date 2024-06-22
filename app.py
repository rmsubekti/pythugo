from flask import Flask
from flask_migrate import Migrate

from models.base import db
from models.oauth import oauth
from routes.author_bp import author_bp
from routes.blog_bp import blog_bp
from routes.auth_bp import auth_bp
from routes.index_bp import index_bp

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

oauth.init_app(app)

app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(author_bp, url_prefix='/author')
app.register_blueprint(blog_bp, url_prefix='/blog')

if __name__ == '__main__':
    app.debug = True
    app.run()