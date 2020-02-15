from app import app, db
from app.models import User, Post

@app.shell_context_processor
def makeShellContext():
    return {"db": db, "User": User, "Post": Post}