import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

from django.contrib.auth.models import User
from djangoapp.populate import initiate

def setup():
    # 1. Populate cars and models
    initiate()

    # 2. Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123')
        admin.first_name = 'Site'
        admin.last_name = 'Admin'
        admin.save()
        print("Superuser 'admin' created successfully.")
    else:
        u = User.objects.get(username='admin')
        u.set_password('adminpassword123')
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print("Superuser 'admin' password updated.")

    # 3. Create regular test user
    if not User.objects.filter(username='testuser').exists():
        u = User.objects.create_user('testuser', 'testuser@example.com', 'testpassword123')
        u.first_name = 'John'
        u.last_name = 'Doe'
        u.save()
        print("Test user 'testuser' created.")
    else:
        u = User.objects.get(username='testuser')
        u.set_password('testpassword123')
        u.save()
        print("Test user 'testuser' password updated.")

if __name__ == '__main__':
    setup()
