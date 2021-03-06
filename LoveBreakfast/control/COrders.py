# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok
import datetime

class COrders():

    def __init__(self):
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

    def get_order_list(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss

        Uid = args["token"]
        # 暂时不处理过滤
        from services.SOrders import SOrders
        sorders = SOrders()
        order_list = sorders.get_all_order_by_uid(Uid)
        data = []
        for row in order_list:
            data_item = {}
            data_item["Oid"] = row.Oid
            print str(row.Otime)
            Otime = row.Otime
            data_item["Otime"] = self.deal_string_to_time(str(Otime))
            data_item["Ostatus"] = self.get_status_name_by_status(row.Ostatus)
            data_item["Oprice"] = row.Oprice
            data_item["Opic"] = row.Opic
            dt = datetime.datetime.now()
            day = datetime.datetime.now().day + 1
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            month_day_list = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0:
                if year % 100 != 0:
                    month_day_list[2] = 29
                if year % 400 == 0:
                    month_day_list[2] = 29
            if day > month_day_list[month]:
                month = month + 1
                day = day - month_day_list[month]
                if month > 12:
                    month = 1
                    year = year + 1
            dt_pass = datetime.datetime(year, month, day, 6, 0, 0)
            if (dt_pass - dt).seconds < 28800 or row.Ostatus > 21 or row.Ostatus == 0:
                data_item["is_index"] = 702
            else:
                data_item["is_index"] = 701
            data_item["Order_items"] = []
            order_items = sorders.get_order_item_by_oid(row.Oid)
            from services.SProduct import SProduct
            sproduct = SProduct()
            for raw in order_items:
                order_item = {}
                order_item["Pnum"] = raw.Pnum
                Pid = raw.Pid
                product = sproduct.get_product_all_by_pid(Pid)
                order_item["Pname"] = product.Pname
                order_item["Psalenum"] = product.P_sales_volume
                order_item["Plevel"] = product.Pscore
                order_item["Pprice"] = product.Pprice
                order_item["Pimage"] = product.Pimage
                data_item["Order_items"].append(order_item)
            data.append(data_item)

        response_make_main_order = {}
        response_make_main_order["status"] = response_ok
        response_make_main_order["messages"] = ""
        response_make_main_order["data"] = data
        return response_make_main_order

    def get_order_abo(self):
        args = request.args.to_dict()
        if "token" not in args or "Oid" not in args:
            return self.param_miss
        Oid = args["Oid"]
        Uid = args["token"]
        from services.SOrders import SOrders
        sorders = SOrders()
        order_abo = sorders.get_order_abo_by_oid(Oid)
        data = {}
        data["Oid"] = Oid
        data["Otime"] = self.deal_string_to_time(order_abo.Otime)
        data["Ostatus"] = self.get_status_name_by_status(order_abo.Ostatus)
        data["Oprice"] = order_abo.Oprice
        data["Opic"] = order_abo.Opic
        Lid = order_abo.Lid
        labo = sorders.get_lname_lno_lboxno_by_lid(Lid)
        data["Lname"] = labo.Lname
        data["Lno"] = labo.Lno
        data["Lboxno"] = labo.Lboxno
        dt = datetime.datetime.now()
        day = datetime.datetime.now().day + 1
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        month_day_list = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0:
            if year % 100 != 0:
                month_day_list[2] = 29
            if year % 400 == 0:
                month_day_list[2] = 29
        if day > month_day_list[month]:
            month = month + 1
            day = day - month_day_list[month]
            if month > 12:
                month = 1
                year = year + 1
        dt_pass = datetime.datetime(year, month, day, 6, 0, 0)
        if (dt_pass - dt).seconds < 28800 or order_abo.Ostatus > 21 or order_abo.Ostatus == 0:
            data["is_index"] = 702
        else:
            data["is_index"] = 701
        from services.SUsers import SUsers
        susers = SUsers()
        users = susers.get_uname_utel_by_uid(Uid)
        data["Utel"] = users.Utel
        data["Uname"] = users.Uname
        data["Oabo"] = order_abo.Oabo
        data["Order_items"] = []
        order_items = sorders.get_order_item_by_oid(Oid)
        for row in order_items:
            order_item = {}
            order_item["Pnum"] = row.Pnum
            order_item["Pid"] = row.Pid
            from services.SProduct import SProduct
            sproduct = SProduct()
            product = sproduct.get_product_all_by_pid(row.Pid)
            order_item["Pname"] = product.Pname
            order_item["Psalenum"] = product.P_sales_volume
            order_item["Plevel"] = product.Pscore
            order_item["Pprice"] = product.Pprice
            order_item["Pimage"] = product.Pimage
            data["Order_items"].append(order_item)

        response_make_main_order = {}
        response_make_main_order["status"] = response_ok
        response_make_main_order["messages"] = ""
        response_make_main_order["data"] = data
        return response_make_main_order

    def make_main_order(self):
        args = request.args.to_dict()
        data = request.data
        data = json.loads(data)

        if "token" not in args:
            return self.param_miss

        if "Otime" not in data or "Omintime" not in data or "Omaxtime" not in data:
            return self.param_miss

        if "Order_items" not in data:
            return self.system_error
        Uid = args["token"]
        Otime = data["Otime"]
        Otruetimemin = data["Omintime"]
        Otruetimemax = data["Omaxtime"]
        Ostatus = 7

        if "Lname" not in data or "Lno" not in data or "Lboxno" not in data:
            from config.status import response_error
            from config.status_code import error_no_location
            from config.messages import messages_no_location
            no_location = {}
            no_location["status"] = response_error
            no_location["status_code"] = error_no_location
            no_location["messages"] = messages_no_location
            return no_location

        Lname = data["Lname"]
        Lno = data["Lno"]
        Lboxno = data["Lboxno"]

        from services.SOrders import SOrders
        sorders = SOrders()
        Lid = sorders.get_lid_by_lname_lno_lboxno(Lname, Lno, Lboxno)
        if not Lid:
            return self.system_error
        Oabo = None
        if "Oabo" in data:
            Oabo = data["Oabo"]

        add_main_order = sorders.add_main_order(Otime, Otruetimemin, Otruetimemax, Ostatus, None, Uid, Lid, Oabo)
        if not add_main_order:
            return self.system_error

        order_item = data["Order_items"]
        add_order_items_by_uid = self.add_order_items(order_item, add_main_order)

        from config.messages import messages_add_main_order_success
        response_make_main_order = {}
        response_make_main_order["status"] = response_ok
        response_make_main_order["messages"] = messages_add_main_order_success
        return response_make_main_order

    def add_order_items(self, order_item_list, oid):

        #order_item_list = json.loads(order_item_list)
        order_price = 0
        from services.SOrders import SOrders
        sorders = SOrders()
        for row in order_item_list:
            Pid = row["Pid"]
            Pnum = row["Pnum"]
            add_order_item = sorders.add_order_item(oid, Pid, Pnum)
            if not add_order_item:
                return self.system_error
            from services.SProduct import SProduct
            sproduct = SProduct()
            order_item_price = sproduct.get_pprice_by_pid(Pid)
            if not order_item_price:
                from config.status import response_system_error
                from config.messages import error_system_error
                system_error = {}
                system_error["status"] = response_system_error
                system_error["messages"] = error_system_error
                return system_error
            order_price = order_price + order_item_price

        from services.SOrders import SOrders
        sorders = SOrders()
        update_main_order = {}
        update_main_order["Oprice"] = order_price
        response_update_main_order = sorders.update_price_by_oid(oid, update_main_order)

        if not response_update_main_order:
            return self.system_error

        return True

    def update_order_info(self):
        pass

    def update_order_status(self):
        args = request.args.to_dict()
        data = request.data
        data = json.loads(data)

        if "token" not in args:
            return self.param_miss
        if "Ostatus" not in data or "Oid" not in data:
            return self.param_miss

        from services.SOrders import SOrders
        sorders = SOrders()
        # 处理token过程，这里未设计

        Ostatus = data["Ostatus"]

        Ostatus_list = ["已取消", "未支付", "已支付", "已接单", "已配送", "已装箱", "已完成", "已评价"]
        if Ostatus not in Ostatus_list:
            from config.status import response_error
            from config.status_code import error_wrong_status_code
            from config.messages import messages_error_wrong_status_code
            wrong_status_code = {}
            wrong_status_code["status"] = response_error
            wrong_status_code["status_code"] = error_wrong_status_code
            wrong_status_code["messages"] = messages_error_wrong_status_code
            return wrong_status_code
        Oid = data["Oid"]

        update_ostatus = {}
        update_ostatus["Ostatus"] = self.get_status_by_status_name(Ostatus)

        response_update_order_status = sorders.update_status_by_oid(Oid, update_ostatus)

        if not response_update_order_status:
            return self.system_error

        from config.messages import messages_update_order_status_ok
        update_order_status_ok = {}
        update_order_status_ok["status"] = response_ok
        update_order_status_ok["messages"] = messages_update_order_status_ok

        return update_order_status_ok

    def get_order_user(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss
        Uid = args["token"]

        from services.SUsers import SUsers
        susers = SUsers()
        users_info = susers.get_all_users_info(Uid)

        if not users_info:
            return self.system_error

        response_user_info = {}
        Utel = users_info.Utel
        response_user_info["Utel"] = Utel
        if users_info.Uname not in ["", None]:
            Uname = users_info.Uname
            response_user_info["Uname"] = Uname
        else:
            response_user_info["Uname"] = None
        if users_info.Usex not in ["", None]:
            Usex = users_info.Usex
            response_user_info["Usex"] = Usex
        else:
            response_user_info["Usex"] = None

        response_of_get_all = {}
        response_of_get_all["status"] = response_ok
        from config.messages import messages_get_item_ok
        response_of_get_all["messages"] = messages_get_item_ok
        response_of_get_all["data"] = response_user_info
        return response_of_get_all

    def get_status_name_by_status(self, status):
        status_name = ["已取消", "未支付", "已支付", "已接单", "已配送", "已装箱", "已完成", "已评价"]
        return status_name[status/7]

    def get_status_by_status_name(self, status_name):
        status_list = ["已取消", "未支付", "已支付", "已接单", "已配送", "已装箱", "已完成", "已评价"]
        i = 0
        while i < 7:
            if status_name == status_list[i]:
                return i*7
            i = i + 1

        return -99

    def deal_time_to_string(self, time):
        time_string = str(time[0,3]) + str(time[5,6]) + str(time[8,9]) + str(time[11,12]) + str(time[14,15]) + \
                      str(time[17,18])
        return time_string
    def deal_string_to_time(self, time_string):
        # time_string = int(time_string)
        time = time_string[0]\
               + time_string[1]\
               + time_string[2]\
               + time_string[3]\
               + "-" \
               + time_string[4]\
               + time_string[5]\
               + "-" \
               + time_string[6]\
               + time_string[7]\
               + " " \
               + time_string[8]\
               + time_string[9]\
               + ":" \
               + time_string[10] \
               + time_string[11]\
               + ":" \
               + time_string[12] \
               + time_string[13]
        return time

if __name__ == "__main__":
    sorder = COrders()
    print sorder.get_status_by_status_name("未支付")