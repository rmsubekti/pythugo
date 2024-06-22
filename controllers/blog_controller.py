import sys
from flask import render_template, redirect, url_for, request, abort, session,g, flash
from controllers.auth_controller import login_required
from sqlalchemy import select, update,text
from models.blog import Blog
from models.author import Author
from models.base import db
from models.oauth import github
import json

@login_required
def index():
    result = db.session.execute(text("select * from blog b join blog_author ba on ba.blog_id=b.id where ba.author_id=:id"), {"id": g.user.id}).all()
    db.session.close()
    return render_template("blog/index.html", blogs=result)

@login_required
def create():
    token =g.user.github_token.to_token()
    error = None
    if request.method == "POST":
        repo = request.form["repo"]
        tree = github.get('repos/'+repo, token=token)
        data = tree.json()
        ok = False
        for path in data["tree"]:
            if path["path"] == "content" and path["type"] == "tree":
                ok = True
                break
        if ok :
            v = repo.split("/")
            blog = Blog(name=v[1], branch=v[4],repo=repo, owner_id=g.user.id, authors=[g.user])

            db.session.add(blog)
            db.session.commit()
            return redirect('/blog')
        else:
            error = f"Repo '{repo}' does not have blog content."
    flash(error)
    repos = github.get('user/repos?per_page=100', token=token)
    data= repos.json()
    return render_template("blog/create.html", repos=data)

@login_required
def editor(blog_id):
    blog = db.session.execute(text("select * from blog b join blog_author ba on ba.blog_id=b.id where ba.author_id=:user_id and b.id =:id"), {"user_id": g.user.id, "id":blog_id}).fetchone()
    g.blog = (blog)
    owner=db.session.execute(select(Author).where(Author.id==blog.owner_id)).first()
    g.token = (owner[0].github_token)
    tree = github.get('repos/'+blog.repo, token=owner[0].github_token.to_token())
    repo = tree.json()
    # for d in repo["tree"]:
    #     if d["path"]=="content":
    #         tree = github.get(d["url"]+"?recursive=true", token=owner[0].github_token.to_token())
    #         break
    # data = tree.json()
    # trees = [None] * 6
    # for n in data["tree"]:
    #     if n["type"]=="tree":
    #         n["tree"]=[]
    #     path = n["path"].split("/")
    #     if len(path)>0:
    #         if trees[len(path)-1] == None:
    #             trees[len(path)-1]=[]
    #         trees[len(path)-1].append(n)

    # x = len(trees)-1
    # while x>0:
    #     if trees[x] == None:
    #         x-=1
    #         continue
    #     for y in trees[x]:
    #         path = y["path"].split("/")
    #         sub= "/".join(path[:-1])
    #         for z in trees[x-1]:
    #             if z["path"] == sub:
    #                 z["tree"].append(y)
    #     x-=1
    # content = trees[0]
    return render_template("blog/editor.html", blog=blog, data=repo)

def show(blogId):
    ...

def delete(blogId):
    ...