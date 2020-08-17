from dotenv import load_dotenv
from kingdom_api.app import create_app
from pathlib import Path


env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

app = create_app()
