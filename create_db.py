from pythonic import create_app, db

# Create the Flask application instance
app = create_app()

# Push an application context to make sure db.create_all() runs within it
with app.app_context():
    # Create all database tables
    db.create_all()
