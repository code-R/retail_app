import os
import retailstore.conf.config as config

from werkzeug.serving import run_simple
from paste import deploy


config.config_mgr.register_options()
CONF = config.config_mgr.conf

env = os.environ
dirname = env.get('CONFIG_DIR', '/etc/retailstore').strip()
config_files = [os.path.join(dirname, 'retailstore.conf')]

CONF([], project='retailstore', default_config_files=config_files)

paste_file = CONF.find_file(CONF.api_paste_config)

wsgi_app = deploy.loadapp('config:%s' % paste_file)

run_simple(CONF.bind_host, CONF.bind_port, wsgi_app)
