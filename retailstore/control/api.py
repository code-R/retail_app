import os

from paste import deploy
import retailstore.conf.config as config

config.config_mgr.register_options()
CONF = config.config_mgr.conf

CONFIG_FILES = ['retailstore.conf']

def _get_config_files(env=None):
    if env is None:
        env = os.environ

    config_file = env.get(
        'CONF_FILE', '/etc/retailstore/retailstore.conf').strip()
    return [config_file]

def init_application():
    """Main entry point for initializing the Store API service.

    Create routes for the v1.0 API.
    """
    config_files = _get_config_files()
    CONF([], project='retailstore', default_config_files=config_files)
    paste_file = CONF.find_file(CONF.api_paste_config)

    app = deploy.loadapp('config:%s' % paste_file, name='main')
    return app


if __name__ == '__main__':
    init_application()
