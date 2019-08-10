# -*- coding: utf-8 -*-
# @Time    : 2019/8/10 10:25
# @Author  : Yaojie Chang
# @File    : adminx.py
# @Software: PyCharm
import xadmin
from xadmin import views
from get_ticket.models import VisitTicket, Grab


class BaseSetting(object):
    enable_themes = True    # 允许使用主题
    use_bootswatch = True   # 增加主题


# 全局设置
class GlobalSettings(object):
    site_title = '抢票管理'    # 标题
    site_footer = '随之风'         # 页脚
    menu_style = 'accordion'        # 菜单风格


# 数据库注册到admin
class GrabAdmin(object):
    list_display = ['name', 'stu_id', 'major', 'is_success', 'is_checked', 'times', 'ticket_id']
    search_fields = ['name', 'stu_id', 'major', 'is_success', 'times']
    list_filter = ['name', 'stu_id', 'major', 'is_success', 'times']


class VisitTicketAdmin(object):
    list_display = ['name', 'stu_id', 'major', 'is_success', 'times']
    search_fields = ['name', 'stu_id', 'major', 'is_success', 'times']
    list_filter = ['name', 'stu_id', 'major', 'is_success', 'times']


xadmin.site.register(Grab, GrabAdmin)
xadmin.site.register(VisitTicket, VisitTicketAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
