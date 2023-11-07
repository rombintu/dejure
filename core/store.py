from core.tools import logger as log
from core.models import User, Contact, user_build_from_dict

from pymongo import MongoClient
from pymongo_inmemory import MongoClient as MongoClientDev

USER_DB = "users"
TASKS_DB = "tasks"
DATABASE = "dejure"

class Database:
    def __init__(self, conn_string="", dev=False):
        if dev:
            self.conn = MongoClientDev()
        else:
            self.conn = MongoClient(conn_string)
        self.db = self.conn[DATABASE]

    def admin_check_from_configure(self, uid: int):
        log.debug(self.admins)
        return uid in self.admins

    def user_get_by_uid(self, uid: int):
        """Проверка наличия пользователя в БД по telegram-id. Вернуть пользователя"""
        data = self.db[USER_DB].find_one({"_uid": int(uid)})
        if not data:
            return None
        return user_build_from_dict(data)

    def sign_up(self, user: User):
        """Регистрация пользователя, вернуть ID. Если такой пользователь есть, иначе создать. Вернуть User"""
        info = self.user_get_by_uid(user.uid)
        log.debug(f"User [{user.to_dict()}] Exist: {False if not info else True}")
        new_user = None
        if not info:
            new_user = self.user_create(user)
        return new_user

    def user_list(self):
        users = self.db[USER_DB].find()
        return [user for user in users]

    
    def user_create(self, user: User):
        result = self.db[USER_DB].insert_one(user.to_dict()).inserted_id
        log.debug(f"Create new user: [_id] {result} [user] {user.to_dict()}")
        return self.user_get_by_uid(user.uid)

    def user_delete_by_uid(self, uid: int):
        log.debug(f"Try deleting users with uid [{uid}]")
        result = self.db[USER_DB].delete_many({"_uid": uid}).raw_result
        log.debug(f"Deleted: {result}")

    def server_info(self):
        return self.conn.server_info()
    
    # def update(self, user_id, failed, field="failed"):
    #     self.db.table_new.update_one(
    #         {"user_id": str(user_id)},
    #         {"$push": {
    #             field: failed
    #             }, 
    #         }, upsert=False)

