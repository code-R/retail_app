import os

from alembic import command as alembic_command
from alembic import config as alembic_config
from alembic import script as alembic_script
from alembic import util as alembic_util
from oslo_config import cfg

import retailstore.conf.config as config

config.config_mgr.register_options()
CONF = config.config_mgr.conf

HEAD_FILENAME = 'HEAD'

def do_alembic_command(config, cmd, *args, **kwargs):
    try:
        getattr(alembic_command, cmd)(config, *args, **kwargs)
    except alembic_util.CommandError as e:
        alembic_util.err(str(e))

def do_upgrade(config, cmd):
    if not CONF.command.revision and not CONF.command.delta:
        raise SystemExit('You must provide a revision or relative delta')

    revision = CONF.command.revision

    if CONF.command.delta:
        revision = '+%s' % str(CONF.command.delta)
    else:
        revision = CONF.command.revision

    do_alembic_command(config, cmd, revision, sql=CONF.command.sql)


def update_head_file(config):
    script = alembic_script.ScriptDirectory.from_config(config)
    if len(script.get_heads()) > 1:
        alembic_util.err('Timeline branches unable to generate timeline')

    head_path = os.path.join(script.versions, HEAD_FILENAME)
    with open(head_path, 'w+') as f:
        f.write(script.get_current_head())


def do_revision(config, cmd):
    do_alembic_command(config, cmd,
                       message=CONF.command.message,
                       autogenerate=CONF.command.autogenerate,
                       sql=CONF.command.sql)
    update_head_file(config)

def add_command_parsers(subparsers):
    for name in ['current', 'history', 'branches']:
        parser = subparsers.add_parser(name)
        parser.set_defaults(func=do_alembic_command)

    parser = subparsers.add_parser('check_migration')
    parser.set_defaults(func=do_check_migration)

    parser = subparsers.add_parser('upgrade')
    parser.add_argument('--delta', type=int)
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_upgrade)

    parser = subparsers.add_parser('stamp')
    parser.add_argument('--sql', action='store_true')
    parser.add_argument('revision')
    parser.set_defaults(func=do_stamp)

    parser = subparsers.add_parser('revision')
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true')
    parser.add_argument('--sql', action='store_true')
    parser.set_defaults(func=do_revision)

    parser = subparsers.add_parser('purge_deleted')
    parser.set_defaults(func=purge_deleted)
    # positional parameter
    parser.add_argument(
        'resource',
        choices=['all', 'events', 'vnf', 'vnfd', 'vims'],
        help='Resource name for which deleted entries are to be purged.')
    # optional parameter, can be skipped. default='90'
    parser.add_argument('-a', '--age', nargs='?', default='90',
                        help='How long to preserve deleted data, '
                             'defaults to 90')
    # optional parameter, can be skipped. default='days'
    parser.add_argument(
        '-g', '--granularity', default='days',
        choices=['days', 'hours', 'minutes', 'seconds'],
        help='Granularity to use for age argument, defaults to days.')


command_opt = cfg.SubCommandOpt('command',
                                title='Command',
                                help='Available commands',
                                handler=add_command_parsers)

CONF.register_cli_opt(command_opt)


def main():
    config = alembic_config.Config(
        os.path.join(os.path.dirname(__file__), 'alembic.ini')
    )
    config.set_main_option('script_location',
                           'retailstore.db.migration:alembic_migrations')
    # env = os.environ
    # dirname = env.get('CONFIG_DIR', '/etc/retailstore').strip()
    # config_files = [os.path.join(dirname, 'retailstore.conf')]

    # CONF([], project='retailstore', default_config_files=config_files)
    CONF()
    config.store_config = CONF

    CONF.command.func(config, CONF.command.name)
