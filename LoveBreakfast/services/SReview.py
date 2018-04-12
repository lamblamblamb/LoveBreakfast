# *- coding:utf8 *-
# 兼容linux系统
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
# 引用项目类
from models import model
import DBSession
from common.TransformToList import trans_params


# 操作user表的相关方法
class SReview():
    def __init__(self):
        """
        self.session 数据库连接会话
        self.status 判断数据库是否连接无异常
        """
        self.session, self.status = DBSession.get_session()
        pass

    # 创建评论
    def create_review(self,review):
        try:
            self.session.add(review)
        except Exception as e:
            print e.message
        finally:
            self.session.close()

    # 根据用户id获取评论信息
    def get_user_review(self, uid):
        try:
            review_of_service = self.session.query(model.Review.Rid, model.Review.Rscore, model.Review.Rpname, model.Review.Rpimage,
                                                   model.Review.Rcontent).filter_by(Uid=uid).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return review_of_service

    # 根据用户id获取评论id列表
    def get_rid_by_uid(self, uid):
        try:
            review_list = self.session.query(model.Review.Rid).filter_by(Uid=uid).all()
        except Exception as e:
            print e.message
        finally:
            self.session.close()
        return review_list