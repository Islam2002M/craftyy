
from pythonic.models import User
def get_plumbing_users_from_database():
    # Query users with service type of plumbing
    plumbing_users = User.query.filter_by(service_type='plumbing').all()

    return plumbing_users
