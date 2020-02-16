from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt


@login.user_loader
def loadUser(id):
    return User.query.get(int(id))


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        "User", secondary = followers, 
        primaryjoin=(followers.c.follower_id == id), 
        secondaryjoin=(followers.c.followed_id == id), 
        backref = db.backref("followers", lazy="dynamic"), 
        lazy="dynamic"
    )

    def __repr__(self):
        return "<User: {}>".format(self.username)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.isFollowing(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.isFollowing(user):
            self.followed.remove(user)

    def isFollowing(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followedPosts(self):
        othersPosts = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        ownPosts = Post.query.filter_by(user_id = self.id)
        return othersPosts.union(ownPosts).order_by(Post.timestamp.desc())
    
    def getResetPasswordToken(self, expiresIn = 600):
        return jwt.encode(
            {"resetPassword":self.id, "exp":time() + expiresIn},
            app.config["SECRET_KEY"],
            algorithm = "HS256"
        ).decode("utf-8")

    @staticmethod
    def verifyResetPasswordToken(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms = ["HS256"])["resetPassword"]
        except:
            return
        return User.query.get(id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post: {} by User: {}>".format(self.body, self.user_id)