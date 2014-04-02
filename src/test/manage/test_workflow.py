
from sqlalchemy import create_engine

from manage import generate_post, publish_post, delete_post
from web.db import get_db
from web.models import Base
from test.generate_tools import generate_post as dummy_post

class TestPostWorkFlow(object):
    @classmethod
    def setup_class(cls):
        db = get_db()
        Base.metadata.create_all(db.engine)

    @classmethod
    def teardown_class(cls):
        db = get_db()
        Base.metadata.drop_all(db.engine)

    def test_workflow(self):
        " Tests post generation, publishing, and deletion "
        p = dummy_post("nezaj", "Moop")
        generate_post(p, force=True)
        publish_post(p, force=True)
        delete_post(p)
