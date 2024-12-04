from logger import init_sentry
from services.api_server.api import app

init_sentry()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
