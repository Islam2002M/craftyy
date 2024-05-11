
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
