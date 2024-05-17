
from pythonic.models import User
def get_plumbing_users_from_database():
    # Query users with service type of plumbing
    plumbing_users = User.query.filter_by(service_type='plumbing').all()

    return plumbing_users
def get_electrical_users_from_database():
    # Query users with service type of electrical
    electrical_users = User.query.filter_by(service_type='electrical').all()

    return electrical_users
def get_cleaning_users_from_database():
    # Query users with service type of cleaning
    cleaning_users = User.query.filter_by(service_type='Cleaning').all()

    return cleaning_users

def get_movingFur_users_from_database():
    # Query users with service type of plumbing
    movingFur_users = User.query.filter_by(service_type='Moving Furniture').all()

    return movingFur_users

def get_Painting_users_from_database():
    # Query users with service type of plumbing
    Painting_users = User.query.filter_by(service_type='Painting').all()

    return Painting_users

def get_Carpentry_users_from_database():
    # Query users with service type of plumbing
    Carpentry_users = User.query.filter_by(service_type='Carpentry').all()

    return Carpentry_users
