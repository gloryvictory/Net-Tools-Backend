## https://www.devdungeon.com/content/run-python-wsgi-web-app-waitress

from waitress import serve
import app
serve(app.app, host='::1', port=5000)
