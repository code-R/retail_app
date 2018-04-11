# # from oslo_config import cfg
# import os
# import retailstore.conf.config as config

# config.config_mgr.register_options()

# CONF = config.config_mgr.conf

# CONFIG_FILES = ['retailstore.conf', 'retailstore-paste.ini']


# env = os.environ
# dirname = env.get('CONFIG_DIR', '/etc/retailstore').strip()
# config_files = [
#     os.path.join(dirname, config_file)
#     for config_file in CONFIG_FILES
# ]


# CONF([], project='retailstore', default_config_files=config_files)
# res = CONF
# paste_file = res.find_file(CONF.api_paste_config)
