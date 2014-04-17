from manage import generate_post, publish_post, delete_post
from web.loggers import get_stderr_logger
from data.db import get_db
from data.models import Base
from test.generate_tools import generate_post as dummy_post

class TestPostWorkFlow(object):
    @classmethod
    def setup_class(cls):
        cls.db = get_db()
        Base.metadata.create_all(cls.db.engine)

    @classmethod
    def teardown_class(cls):
        Base.metadata.drop_all(cls.db.engine)

    # I want a fresh db every time I run a test
    # pylint: disable=R0201
    def test_workflow(self):
        " Tests post generation, publishing, and deletion "
        p = dummy_post("nezaj", "Moop")
        logger = get_stderr_logger()

        generate_post(p, logger, force=True)
        publish_post(p, logger, force=True)
        delete_post(p, logger)
