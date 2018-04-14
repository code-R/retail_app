import os

from gabbi import driver
from gabbi.driver import test_pytest  # noqa

from retailstore.db.sqlalchemy import models
from retailstore.db.sqlalchemy import api as db_api

TESTS_DIR = 'gabbits'

def purge_data():
    meta = models.Base.metadata
    session = db_api.get_session()

    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()

# Make sure we start with empty database
purge_data()
def pytest_generate_tests(metafunc):
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    driver.py_test_generator(
        test_dir,
        url=os.environ['TEST_URL'],
        host='localhost',
        metafunc=metafunc
    )
