
from services.api_server.api import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0:8080')
