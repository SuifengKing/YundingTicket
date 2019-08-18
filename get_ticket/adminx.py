# -*- coding: utf-8 -*-
# @Time    : 2019/8/10 10:25
# @Author  : Yaojie Chang
# @File    : adminx.py
# @Software: PyCharm
import xadmin
from xadmin import views
from get_ticket.models import VisitTicket, Grab
from extra_apps.my_xadmin_view import TicketAdminView, TicketControlView, SaveToDatabaseView


class BaseSetting(object):
    enable_themes = True    # 允许使用主题
    use_bootswatch = True   # 增加主题


# 全局设置
class GlobalSettings(object):
    site_title = '抢票管理'    # 标题
    site_footer = '随之风'         # 页脚
    menu_style = 'accordion'        # 菜单风格

    # 设计左侧菜单
    def get_site_menu(self):  # 名称不能改
        return [
            {
                'title': '票务管理',
                'icon': 'fa fa-bar-chart-o',
                'menus': (
                    {
                        'title': '余票及抢票情况',    # 这里是你菜单的名称
                        'url': '/xadmin/ticket_info',     # 这里填写你将要跳转url
                        'icon': 'fa fa-bars'     # 这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },
                    {
                        'title': 'Redis余票管理',  # 这里是你菜单的名称
                        'url': '/xadmin/ticket_control',  # 这里填写你将要跳转url
                        'icon': 'fa fa-bars'  # 这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },
                    {
                        'title': '数据转存',  # 这里是你菜单的名称
                        'url': '/xadmin/save_to_db',  # 这里填写你将要跳转url
                        'icon': 'fa fa-bars'  # 这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },
                )
            }
        ]


# 注册你上面填写的url
xadmin.site.register_view(r'ticket_info/', TicketAdminView, name='ticket_admin')
xadmin.site.register_view(r'ticket_control/', TicketControlView, name='ticket_control_admin')
xadmin.site.register_view(r'save_to_db/', SaveToDatabaseView, name='save_to_database')


# 数据库注册到admin
class GrabAdmin(object):
    list_display = ['name', 'stu_id', 'major', 'is_success', 'is_checked', 'times', 'ticket_id']
    search_fields = ['name', 'stu_id', 'major', 'is_success', 'times']
    list_filter = ['name', 'stu_id', 'major', 'is_success', 'times']


class VisitTicketAdmin(object):
    list_display = ['name', 'stu_id', 'major', 'is_success', 'is_checked', 'times', 'ticket_id']
    search_fields = ['name', 'stu_id', 'major', 'is_success', 'times']
    list_filter = ['name', 'stu_id', 'major', 'is_success', 'times']


xadmin.site.register(Grab, GrabAdmin)
xadmin.site.register(VisitTicket, VisitTicketAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
