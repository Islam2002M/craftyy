from datetime import datetime
from pythonic import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="prf.jpg")
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(25), nullable=False)
    contactNumber = db.Column(db.String(10), nullable=False)  # Assuming mobile number is 10 digits long
    user_type = db.Column(db.String(20), nullable=False)
    service_type = db.Column(db.String(20), nullable=True)  # Set nullable to True
    description = db.Column(db.Text, nullable=True)  # Set nullable to True
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=True)
    works=db.relationship("Work", backref="maker", lazy=True)
    # lessons = db.relationship("Lesson", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    img = db.Column(db.String(20), nullable=False, default="default_thumbnail.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

    def __repr__(self):
        return f"Lesson('{self.title}', '{self.date_posted}')"


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)  # Set nullable to True
    image_ser = db.Column(db.String(20), nullable=False, default="default.jpg")
    UserProvides = db.relationship("User", backref="provider", lazy=True)
    #lessons = db.relationship("Lesson", backref="course_name", lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serviceName = db.Column(db.String(50), unique=True, nullable=False)
    Needs = db.Column(db.Text, nullable=False)  # Set nullable to True
    UserProvides = db.relationship("User", backref="provider", lazy=True)
    #lessons = db.relationship("Lesson", backref="course_name", lazy=True)

    def __repr__(self):
        return f"Service('{self.Name}')"