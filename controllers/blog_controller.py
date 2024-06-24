import sys
import os
import base64
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
    error = ""
    if request.method == "POST":
        try:
            repo = request.form["repo"]
            tree = github.get('repos/'+repo, token=token)
            data = tree.json()
            if not tree.ok:
                raise ValueError

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
        except ValueError:
            error = "empty repository"
        else:
            print("something wrong")

    if error:
        flash(error)
        
    repos = github.get('user/repos?per_page=100', token=token)
    data= repos.json()
    return render_template("blog/create.html", repos=data)

@login_required
def editor(blog_id):
    blog = db.session.execute(text("select * from blog b join blog_author ba on ba.blog_id=b.id where ba.author_id=:user_id and b.id =:id"), {"user_id": g.user.id, "id":blog_id}).fetchone()
    owner=db.session.execute(select(Author).where(Author.id==blog.owner_id)).first()
    tree = github.get('repos/'+blog.repo, token=owner[0].github_token.to_token())
    repo = tree.json()
    for item in repo["tree"]:
        if item["path"] == "content" and item["type"]=="tree":
            url = "repos/"+"/".join(blog.repo.split("/")[:-1])+"/"+item["sha"]
            tree = github.get(url+"?recursive=true", token=owner[0].github_token.to_token())
            break
    repo = tree.json()

    # sort the tree 
    trees = [None] * 10
    for n in repo["tree"]:
        n["path"]="content/"+n["path"]
        n["name"]=n["path"].split("/")[-1]
        if n["type"]=="tree":
            n["tree"]=[]
        path = n["path"].split("/")
        if len(path)>0:
            if trees[len(path)-1] == None:
                trees[len(path)-1]=[]
            trees[len(path)-1].append(n)

    # create node tree
    x = len(trees)-1
    while x>0:
        if trees[x] == None:
            x-=1
            continue
        for y in trees[x]:
            path = y["path"].split("/")
            sub= "/".join(path[:-1])
            if trees[x-1] == None:
                continue
            for z in trees[x-1]:
                if z["path"] == sub:
                    z["tree"].append(y)
        x-=1
    return render_template("blog/editor.html", blog=blog, data=trees[1])

@login_required
def getBlob(blog_id, sha):
    blog = db.session.execute(text("select * from blog b join blog_author ba on ba.blog_id=b.id where ba.author_id=:user_id and b.id =:id"), {"user_id": g.user.id, "id":blog_id}).fetchone()
    owner=db.session.execute(select(Author).where(Author.id==blog.owner_id)).first()
    url = "repos/"+"/".join(blog.repo.split("/")[:-2])+"/blobs/"+sha
    blob = github.get(url, token=owner[0].github_token.to_token())
    result = blob.json()
    result["content"]= base64.b64decode(result["content"]).decode()
    return result

@login_required
def saveBlob(blog_id, sha):
    body = request.json
    pathName = body["path"]
    content = base64.b64encode(bytes(body["content"],"utf-8")).decode('utf-8')
    blog = db.session.execute(text("select * from blog b join blog_author ba on ba.blog_id=b.id where ba.author_id=:user_id and b.id =:id"), {"user_id": g.user.id, "id":blog_id}).fetchone()
    owner=db.session.execute(select(Author).where(Author.id==blog.owner_id)).first()
    url = "repos/"+"/".join(blog.repo.split("/")[:-3])+"/contents/"+pathName
    payload = {'message': 'update '+pathName, 'committer': {'name':os.getenv("COMMITTER_NAME"),'email':os.getenv("COMMITTER_EMAIL")}, 'content':content, 'sha':sha}
    blob = github.put(url, token=owner[0].github_token.to_token(), json=payload)
    result = blob.json()
    return result

def show(blogId):
    ...

def delete(blogId):
    ...