from core.store import Database
from core.models import User, Contact, user_build_from_message
# from core.async_bot import run, log
from core.tools import logger as log
from core.tools import Config
from core.tools import get_args
import sys


db = None
config = None
# Arg parse
if "pytest" not in sys.modules:
    args = get_args()
    path = args.config
    log.info(f"Use config file: [{path}]")
    config = Config(path="config.json")

    if config.debug:
        log.level("DEBUG")
        log.info("log level set: Debug")
    else:
        log.remove()
        log.add(sys.stderr, level="INFO")
        log.info("log level set: Info")

    if config.database.mode == 0:
        log.debug("Starting Database in memory")
        db = Database(conn_string="", dev=True)

    if len(config.admins) == 0:
        log.error("Must specify at least one administrator")
    db.admins = config.admins
    log.info(f"Set admins: {db.admins}")