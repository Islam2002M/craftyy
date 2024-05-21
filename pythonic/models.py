from datetime import datetime, timedelta
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
    availability = db.relationship('Availability', uselist=False, backref='owner', lazy=True)  # One-to-one relationship
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



    def __repr__(self):
        return f"Service('{self.Name}')"
    
class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    days = db.Column(db.String(10), nullable=False)  # Assuming this is what you mean by 'days'
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    slots = db.relationship('Slot', backref='availability', lazy=True)
    
    def generate_slots(self, duration):
        """Generate slots based on start_time, end_time, and duration in minutes."""
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        slot_duration = timedelta(minutes=duration)

        current_time = start
        while current_time + slot_duration <= end:
            period = f"{current_time.time()}-{(current_time + slot_duration).time()}"
            slot = Slot(period=period, duration=duration, availability_id=self.id)
            db.session.add(slot)
            current_time += slot_duration

    def __repr__(self):
        return f"Availability('{self.start_time}', '{self.end_time}', '{self.days}')"

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Define duration column
    availability_id = db.Column(db.Integer, db.ForeignKey('availability.id'), nullable=False)

    def __repr__(self):
        return f"Slot('{self.id}', '{self.period}')"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    craft_owner = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False) 
    appointment_purpose = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Appointment {self.first_name} {self.last_name} on {self.appointment_date} at {self.appointment_time}>"