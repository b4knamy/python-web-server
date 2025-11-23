import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000


THROTTLE_REQUESTS_LIMIT = 5
THROTTLE_REQUESTS_TIMEOUT = 60
