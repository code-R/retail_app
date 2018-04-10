from oslo_config import cfg


class AppConfig(object):
    """Initialize all the core options."""

    # Default options
    options = [
        cfg.IntOpt(
            'some_default_option',
            default=10,
            help='Just some config options'
        ),
    ]

    # Database options
    database_options = [
        cfg.StrOpt(
            'database_connect_string',
            help='The URI database connect string.'),
    ]

    def __init__(self):
        self.conf = cfg.CONF

    def register_options(self):
        self.conf.register_opts(AppConfig.options)
        self.conf.register_opts(AppConfig.database_options, group='database')


config_mgr = AppConfig()


def list_opts():
    """Used by oslo config generator."""
    opts = {
        'DEFAULT': AppConfig.options,
        'database': AppConfig.database_options,
    }

    return _tupleize(opts)


def _tupleize(d):
    """Convert a dict of options to the 2-tuple format."""
    return [(key, value) for key, value in d.items()]
