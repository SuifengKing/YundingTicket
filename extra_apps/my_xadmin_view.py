# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 16:15
# @Author  : Yaojie Chang
# @File    : my_xadmin_view.py
# @Software: PyCharm
from django.shortcuts import render, redirect
from django.views import View
from xadmin.views import CommAdminView

import random
import redis

from get_ticket.models import Grab, VisitTicket


class TicketAdminView(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "Redis余票及抢票情况"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了

        preach_times_dict = {'1': '12:30', '2': '19:30'}
        visit_times_dict = {
            '8': '8:30-10:00',
            '10': '10:00-12:00',
            '12': '12:30-14:00',
            '14': '14:00-16:00',
            '16': '16:00-18:00',
            '18': '18:00-19:00',
            '19': '19:00-20:00',
            '20': '20:00-21:00',
            '21': '21:00-22:00'
        }
        r = redis.StrictRedis(decode_responses=True)
        preach_users_keys = r.keys('G-U-*')
        preach_users_num = len(preach_users_keys)
        visit_users_keys = r.keys('V-U-*')
        visit_users_num = len(visit_users_keys)
        preach_available_tickets = {}
        visit_available_tickets = {}
        for time_code, times in preach_times_dict.items():
            preach_available_tickets[times] = r.llen('G-'+time_code+'-tickets')
        for time_code, times in visit_times_dict.items():
            visit_available_tickets[times] = r.llen('V-'+time_code+'-tickets')
        context['preach_users_num'] = preach_users_num
        context['visit_users_num'] = visit_users_num
        context['preach_available_tickets'] = preach_available_tickets
        context['visit_available_tickets'] = visit_available_tickets
        return render(request, 'ticket_info.html', context)  # 最后指定自定义的template模板，并返回context


class TicketControlView(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "Redis余票管理"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了

        preach_times_dict = {'1': '12:30', '2': '19:30'}
        visit_times_dict = {
            '8': '8:30-10:00',
            '10': '10:00-12:00',
            '12': '12:30-14:00',
            '14': '14:00-16:00',
            '16': '16:00-18:00',
            '18': '18:00-19:00',
            '19': '19:00-20:00',
            '20': '20:00-21:00',
            '21': '21:00-22:00'
        }
        context['visit_times_dict'] = visit_times_dict
        return render(request, 'ticket_control.html', context)  # 最后指定自定义的template模板，并返回context

    def post(self, request):
        r = redis.StrictRedis(decode_responses=True)
        r.flushall()
        r.close()
        preach1_num = int(request.POST.get('preach1', '200'))
        preach2_num = int(request.POST.get('preach2', '200'))
        self.add_preach_ticket([('1', preach1_num), ('2', preach2_num)])
        visit_ticket_num_list = list()
        for i in range(8, 22):
            visit_ticket_num_list.append((str(i), int(request.POST.get('visit'+str(i), '0'))))
        self.add_visit_ticket(visit_ticket_num_list)
        return redirect('/xadmin/ticket_info/')

    def add_preach_ticket(self, num=[('1', 20), ('2', 20)]):
        r = redis.StrictRedis(decode_responses=True)
        for times in num:
            for key in range(times[1]):
                all_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
                active_code = ''
                for i in range(5):
                    active_code += random.choice(all_char)
                r.lpush('G-' + times[0] + '-tickets', 'G-' + times[0] + '-' + active_code)

    def add_visit_ticket(self, num=[]):
        r = redis.StrictRedis(decode_responses=True)
        for times in num:
            for key in range(times[1]):
                all_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
                active_code = ''
                for i in range(5):
                    active_code += random.choice(all_char)
                r.lpush('V-' + times[0] + '-tickets', 'V-' + times[0] + '-' + active_code)


class SaveToDatabaseView(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "Redis转存MySQL"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面
        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了
        return render(request, 'save_to_db.html', context)  # 最后指定自定义的template模板，并返回context

    def post(self, request):
        r = redis.StrictRedis(decode_responses=True)
        preach_users_keys = r.keys('G-U-*')
        for key in preach_users_keys:
            user_info = r.hgetall(key)
            Grab.objects.create(**user_info)
            r.delete(key)
        visit_users_keys = r.keys('V-U-*')
        for key in visit_users_keys:
            user_info = r.hgetall(key)
            VisitTicket.objects.create(**user_info)
            r.delete(key)
        return redirect('/xadmin/ticket_info/')

