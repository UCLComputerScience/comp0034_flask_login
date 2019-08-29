from app import create_app
import config

app = create_app(config.DevConfig)
app.app_context().push()