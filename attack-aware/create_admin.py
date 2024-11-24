from models import db, User
from werkzeug.security import generate_password_hash

def create_initial_admin():
    # Check if an admin user already exists
    admin_user = User.query.filter_by(email='admin@admin.com').first()
    if not admin_user:
        # Create the admin user with predefined values
        admin_user = User(
            firstName='admin',
            lastName='admin',
            email='admin@admin.com',
            password=generate_password_hash('admin'),  # Use a secure hash for the password
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()

# Run this function to seed the database
if __name__ == "__main__":
    create_initial_admin()
