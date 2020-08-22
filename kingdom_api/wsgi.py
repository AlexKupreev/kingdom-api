from dotenv import load_dotenv
from kingdom_api.app import create_app
from pathlib import Path
from werkzeug.middleware.proxy_fix import ProxyFix


env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
