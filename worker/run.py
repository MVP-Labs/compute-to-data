
from configparser import ConfigParser
from worker.myapp import app
from worker.log import setup_logging
from worker.routes import services
from worker.admin_routes import admin_services
from worker.utils.utilities import prepare_envir_dir

app.register_blueprint(admin_services)
app.register_blueprint(services)

config_parser = ConfigParser()
config_parser.read(app.config['CONFIG_FILE'])
worker_port = config_parser.get('worker', 'port')

setup_logging()
prepare_envir_dir()

if __name__ == '__main__':
    app.run("0.0.0.0", worker_port, debug=True, use_reloader=False)
