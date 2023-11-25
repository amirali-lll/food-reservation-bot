import os 


HOST=os.environ.get('WEB_HOST','localhost')
BASE_URL = f'http://{HOST}:8000/api/v1/'