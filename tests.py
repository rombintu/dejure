from core.models import User, Contact, user_build_from_dict
from core.store import Database
from core.tools import logger as log
from core.tools import Config

config = Config("config.json")
db = Database(dev=True)
db.admins = config.admins

contact_example = Contact(t_name="name", t_phone="8000", t_link="some-ulr.com")
users = [User(uid=i, contact=contact_example) for i in range(1,10)]

def test_get_user():
    user = users[0]
    payload = db.user_get_by_uid(user.uid)
    log.debug(payload)

def test_create_user():
    user = users[1]
    if db.user_get_by_uid(user.uid):
        db.user_delete_by_uid(user.uid)
    log.debug(db.user_create(user))

    payload = db.user_get_by_uid(user.uid)
    log.debug(payload)

def test_delete_user():
    user = users[2]
    db.user_create(user)
    db.user_delete_by_uid(user.uid)

def test_list_user():
    # db.user_create(users[0])
    users = db.user_list()
    log.debug(users)

def test_signup_user():
    user = users[3]
    if db.user_get_by_uid(user.uid):
        db.user_delete_by_uid(user.uid)
    # log.info(user.to_dict())
    users_list = db.user_list()
    log.debug(users_list)
    log.debug(db.sign_up(user))

def test_double_users():
    user = users[4]
    db.sign_up(user)
    assert db.sign_up(user) == None

def test_check_admins():
    log.debug(db.admin_check_from_configure(0))
    log.debug(db.admin_check_from_configure(100))

def test_user_from_dict():
    user = users[6]
    if db.user_get_by_uid(user.uid):
        db.user_delete_by_uid(user.uid)
    log.debug(db.user_create(user))

    payload = db.user_get_by_uid(user.uid)
    log.debug(payload.to_pretty())
