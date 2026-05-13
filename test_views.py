import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from django.test.client import Client
from django.contrib.auth.models import User
import traceback

def test():
    c = Client()
    user = User.objects.first()
    if not user:
        user = User.objects.create_user('testuser', 'test@test.com', 'password')
    c.force_login(user)
    
    urls_to_test = [
        '/',
        '/login/',
        '/register/',
        '/kursus/',
        '/komunitas/',
        '/misi/',
        '/leaderboard/',
        '/pengaturan/',
    ]
    
    for url in urls_to_test:
        print(f"Testing {url} ...")
        try:
            response = c.get(url)
            print(f"Status: {response.status_code}")
            if response.status_code == 500:
                print(response.content.decode('utf-8'))
        except Exception as e:
            print(f"Exception on {url}:")
            traceback.print_exc()

if __name__ == '__main__':
    test()
