from retailstore.control import api


def start_app():
    return api.init_application()


# Callable to be used by uwsgi.
store_callable = start_app()
