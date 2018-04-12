# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok


class CUsers():
    def __int__(self):
        from config.status import response_error
        from config.status_code import error_param_miss
        from config.messages import error_messages_param_miss
        self.param_miss = {}
        self.param_miss["status"] = response_error
        self.param_miss["status_code"] = error_param_miss
        self.param_miss["messages"] = error_messages_param_miss

        from config.status import response_system_error
        from config.messages import error_system_error
        self.system_error = {}
        self.system_error["status"] = response_system_error
        self.system_error["messages"] = error_system_error

        from services.SUsers import SUsers
        self.susers = SUsers()

    def register(self):
        data = request.data
        print(data)

        if "Utel" not in data or "Upwd" not in data:
            return self.param_miss

        list_utel = self.susers.get_all_user_tel()

        if list_utel == False:
            return self.system_error

        if data["Utel"] in list_utel:
            from config.status import response_system_error
            from config.status_code import error_repeat_tel
            from config.messages import messages_repeat_tel
            repeated_tel = {}
            repeated_tel["status"] = response_system_error
            repeated_tel["status_code"] = error_repeat_tel
            repeated_tel["messages"] = messages_repeat_tel
            return repeated_tel

        is_register = self.susers.login_users(data["Utel"], data["Upwd"])
        if is_register:
            from config.messages import messages_regist_ok
            register_ok = {}
            response_ok["status"] = response_ok
            response_ok["messages"] = messages_regist_ok
            return register_ok
        else:
            return self.system_error

    def login(self):
        data = request.data
        print(data)

        if "Utel" not in data or "Upwd" not in data:
            return self.param_miss

        Utel = data["Utel"]
        list_utel = self.susers.get_all_user_tel()

        if list_utel == False:
            return self.system_error

        if Utel not in list_utel:
            from config.status import response_error
            from config.status_code import error_no_utel
            from config.messages import messages_no_user
            no_utel = {}
            no_utel["status"] = response_error
            no_utel["status_code"] = error_no_utel
            no_utel["messages"] = messages_no_user
            return no_utel

        upwd = self.susers.get_upwd_by_utel(Utel)
        if upwd == data["Upwd"]:
            from config.status import response_error
            from config.status_code import error_wrong_pwd
            from config.messages import messages_wrong_pwd
            wrong_pwd = {}
            wrong_pwd["status"] = response_error
            wrong_pwd["status_code"] = error_wrong_pwd
            wrong_pwd["messages"] = messages_wrong_pwd
            return wrong_pwd

        Uid = self.susers.get_uid_by_utel(Utel)

        login_success = {}
        from config.messages import messages_login_ok
        login_success["status"] = response_ok
        login_success["messages"] = messages_login_ok
        login_success["token"] = Uid

        return login_success

    def update_info(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        data = request.data

        if "Uname" not in data and "Usex" not in data:
            return self.param_miss

        users = {}
        if "Uname" in data:
            Uname = data["Uname"]
            users["Uname"] = Uname
        if "Usex" in data:
            Usex = data["Usex"]
            users["Usex"] = Usex

        update_info = self.susers.update_users_by_uid(Uid, users)

        if not update_info:
            return self.system_error

        response_of_update_users = {}
        from config.messages import messages_update_personal_ok
        response_of_update_users["status"] = response_ok
        response_of_update_users["messages"] = messages_update_personal_ok

        return response_of_update_users

    def update_pwd(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        data = request.data

        if "Upwd" not in data:
            return self.param_miss

        users = {}
        Upwd = data["Upwd"]
        users["Upwd"] = Upwd

        update_info = self.susers.update_users_by_uid(Uid, users)

        if not update_info:
            return self.system_error

        response_of_update_users = {}
        from config.messages import messages_update_pwd_ok
        response_of_update_users["status"] = response_ok
        response_of_update_users["messages"] = messages_update_pwd_ok

        return response_of_update_users

    def get_all(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        users_info = self.susers.get_all_users_info(Uid)

        if not users_info:
            return self.system_error

        response_user_info = {}
        Utel = users_info.Utel
        response_user_info["Utel"] = Utel
        if "Uname" in users_info:
            Uname = users_info.Uname
            response_user_info["Uname"] = Uname
        else:
            response_user_info["Uname"] = None
        if "Usex" in users_info:
            Usex = users_info.Usex
            response_user_info["Usex"] = Usex
        else:
            response_user_info["Usex"] = None

        response_of_get_all = {}
        response_of_get_all["status"] = response_ok
        response_of_get_all["messages"] = response_user_info
        