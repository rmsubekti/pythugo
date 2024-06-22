import sys
import functools
from flask import render_template, redirect, url_for, request, abort, flash, g, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.author import Author
from models.github_token import GithubToken
from models.base import db
from models.oauth import github
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from logger import LOGGER

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth_bp.github_login"))
        return view(**kwargs)
    return wrapped_view

def load_logged_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None 
    else:
        res=db.session.execute(select(Author).where(Author.id==user_id)).first()
        g.user = (
            res[0]
        )

def github_login():
    redirect_url = url_for("auth_bp.github_authorize", _external=True)
    return github.authorize_redirect(redirect_url)

def github_authorize():
    token = github.authorize_access_token()
    user = github.get('user', token=token)
    data = user.json()
    github_token= GithubToken(token_type=token["token_type"],access_token=token["access_token"],refresh_token=token["refresh_token"] if "expires_at" in token else None,expires_at=token["expires_at"] if "expires_at" in token else None)
    author= Author(id=data["id"],username=data["login"], name=data["name"],avatar_url=data["avatar_url"],email=data["email"], github_token=github_token)
    # do something with the token and profile
    try:
        exist = db.session.execute(select(Author).where(Author.id==data["id"])).first()
        if exist is None:
            db.session.add(author)
            db.session.commit()
        else:
            db.session.execute(update(GithubToken).where(GithubToken.author_id==author.id).values(token_type=token["token_type"],access_token=token["access_token"],refresh_token=token["refresh_token"] if "expires_at" in token else None,expires_at=token["expires_at"] if "expires_at" in token else None))
            db.session.commit()
            session.clear()
            session["user_id"]= exist[0].id
    except IntegrityError as e:
        LOGGER.error(f"IntegrityError when creating user: {e}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError when creating user: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error when creating user: {e}")
    return redirect('/blog')

def logout():
    session["user_id"]=None
    return redirect(url_for("index_bp.index"))
