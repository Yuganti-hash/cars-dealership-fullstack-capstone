import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

from django.contrib.auth.models import User
from djangoapp.models import CarMake, CarModel
from djangoapp.populate import initiate

def setup():
    # 1. Reset and populate 15 car models
    CarModel.objects.all().delete()
    CarMake.objects.all().delete()
    initiate()

    # 2. Create root superuser (for Task 12 Admin login)
    if not User.objects.filter(username='root').exists():
        root = User.objects.create_superuser('root', 'root@example.com', 'rootpassword123')
        root.first_name = ''
        root.last_name = ''
        root.save()
        print("Superuser 'root' created successfully.")
    else:
        r = User.objects.get(username='root')
        r.set_password('rootpassword123')
        r.first_name = ''
        r.last_name = ''
        r.is_superuser = True
        r.is_staff = True
        r.save()
        print("Superuser 'root' updated.")

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

if __name__ == '__main__':
    setup()
