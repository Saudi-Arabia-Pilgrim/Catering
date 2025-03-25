import os

from dotenv import load_dotenv

load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
SIGNING_KEY = os.getenv("SIGNING_KEY")
DEBUG = os.getenv("DEBUG")
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
REDIS_PORT_URL = os.getenv('REDIS_PORT_URL')

TIME_ZONE = os.getenv("TIME_ZONE")
USE_I18N = os.getenv("USE_I18N")
USE_L10N = os.getenv("USE_L10N")
USE_TZ = os.getenv("USE_TZ")
