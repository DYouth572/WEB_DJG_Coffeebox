import os
import sys
from pathlib import Path
import django

# Ensure project root is on PYTHONPATH so Django can import settings
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ensure we use production-like storage
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DEBUG', '0')

django.setup()

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

User = get_user_model()

def run():
    u, created = User.objects.get_or_create(username='supabase_test', defaults={'email': 'supabase@test.local'})
    # Create a small binary file as placeholder image
    data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 512
    u.avatar.save('test_avatar.png', ContentFile(data), save=True)
    print('Saved avatar for user', u.username)
    try:
        print('Avatar URL:', u.avatar.url)
    except Exception as e:
        print('Cannot read avatar.url:', e)

if __name__ == '__main__':
    run()
