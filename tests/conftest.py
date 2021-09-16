import os
import sys

from django.utils.version import get_version

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# assert get_version() < '3.0.0', 'Пожалуйста, используйте версию Django < 3.0.0'

pytest_plugins = [
    'tests.fixtures.fixture_user',
]
