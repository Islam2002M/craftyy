
from pythonic.models import User
from pythonic import db
# Define descriptions for different plumbing services (adjust as needed)
descriptions = [
  "Experienced plumber specializing in leak detection and repair.",
  "Offering reliable installation and maintenance services for toilets, faucets, and sinks.",
  "Expert in drain cleaning and unclogging for residential and commercial properties.",
  "Providing high-quality water heater installation and repair services.",
  "Specializing in bathroom and kitchen plumbing renovations."
]

# Seed 30 Craft Owner users with Plumbing service
for i in range(1, 31):
  username = f"plumber_{i}"
  email = f"plumber{i}@example.com"
  password = "password123"  # Replace with a strong password hashing mechanism
  address = f"Address {i}"
  contact_number = f"012345678{i}"  # Adjust phone number format
  user_type = "Craft Owner"
  service_type = "Plumbing"
  description = descriptions[i % len(descriptions)]  # Use descriptions cyclically

  user = User(username=username, email=email, password=password, address=address,
              contactNumber=contact_number, user_type=user_type, service_type=service_type,
              description=description)
  db.session.add(user)

db.session.commit()
print("Successfully seeded 30 Craft Owner users with Plumbing service.")
