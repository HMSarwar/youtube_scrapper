DEBUG = True

redbeat_redis_url = "redis://localhost:6379/12"

DEV_API_KEY = 'your api key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'youtube_scrapper',
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'port': '3306',
    }
}

CHANNEL_FILE_PATH = '/{{base_path}}/channels.txt'