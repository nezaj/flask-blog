from config import app_config
from data.models import Base
from commands import publish_post, generate_post
from test.generate_tools import generate_post as dummy_post
from loggers import get_stderr_logger

def prepopulate_db():
    " Prepopulates db with sample data "
    logger = get_stderr_logger()
    for _ in xrange(0, 50):
        p = dummy_post()
        generate_post(p, logger, force=True)
        publish_post(p, logger, force=True)

# TODO: I'm currently not using this, I should either use it or throw it out
def stamp_db():
    """
    Creates alembic_version table if it doesn't already exist
    and stamps it with the head revision
    """
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config(app_config.ALEMBIC_INI_PATH)
    command.stamp(alembic_cfg, "head")

def build_db(engine):
    " Generates db tables based on metadata schema "
    Base.metadata.create_all(engine)
