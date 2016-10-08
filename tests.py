import unittest
import os

import tempfile

import app


class UrlinkTestCase(unittest.TestCase):

    def setUp(self):
        """Deploy the test DB (sqlite).

        """

        self.db_handle, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        with app.app.app_context():
           app.init_db()  # nope

    def tearDown(self):
        """Delete the test DB (sqlite).

        """

        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
