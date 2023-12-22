from django.core.management.utils import get_random_secret_key

with open('key.txt', 'w') as f:
    f.write(get_random_secret_key())