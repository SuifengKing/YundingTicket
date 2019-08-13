from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views import View
# Create your views here.
from get_ticket.models import VisitTicket, Grab
import threading
import redis
import time


r = redis.StrictRedis()


def save_data_to_database(ticket_id, userdata, ticket_type):
    """把数据存入到MySQL数据库"""
    if ticket_type == 'visit':
        visit_ticket = VisitTicket()
        visit_ticket.stu_id = userdata.get('stu_id', '')
        visit_ticket.name = userdata.get('name', '')
        visit_ticket.major = userdata.get('major', '')
        visit_ticket.times = userdata.get('time', '')
        visit_ticket.ticket_id = ticket_id
        if ticket_id is None:
            visit_ticket.is_success = False
        else:
            visit_ticket.is_success = True
        visit_ticket.save()
    else:
        preach_ticket = Grab()
        preach_ticket.stu_id = userdata.get('stu_id', '')
        preach_ticket.name = userdata.get('name', '')
        preach_ticket.major = userdata.get('major', '')
        preach_ticket.times = userdata.get('time', '')
        preach_ticket.ticket_id = ticket_id
        if ticket_id is None:
            preach_ticket.is_success = False
        else:
            preach_ticket.is_success = True
        preach_ticket.save()
    print('---存入成功---')


class IndexView(View):
    """首页"""
    def get(self, request):
        return render(request, 'index.html')


class PreachView(View):
    """宣讲会抢票页面"""
    def get(self, request):
        date = time.strftime("%Y-%m-%d  ", time.gmtime())
        times_dict = {'1': date+'12:30', '2': date+'19:30'}
        return render(request, 'preach.html', {'result': '', 'times_dict': times_dict})


class VisitView(View):
    """参观取票页面"""
    def get(self, request):
        times_dict = {'8': '8:30-10:00', '10': '10:00-12:00', '12': '12:30-14:00'}
        return render(request, 'visit.html', {'result': '', 'times_dict': times_dict})


class GetPreachTicketView(View):
    """抢票后台逻辑"""
    def get(self, request):
        times = request.GET.get('times', '')
        times_dict = {'1': '12:30', '2': '19:30'}
        preach_time = times_dict.get(times, '')
        ticket_id = r.lpop('G-'+times+'-ticket_id')
        if ticket_id is not None:
            ticket_id = ticket_id.decode('utf8')
            name = request.GET.get('name', '')
            stu_id = request.GET.get('stu_id', '')
            major = request.GET.get('major', '')
            userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'time': preach_time}
            save_data_to_database(ticket_id, userdata, 'preach')
            # 抢票成功应该返回学生的相应信息以及票的信息(包括二维码)以便用于检票
            return render(request, 'preach.html', {'result': ticket_id, 'name': name, 'stu_id': stu_id, 'code': 1, 'times': preach_time})
        else:
            name = request.GET.get('name', '')
            stu_id = request.GET.get('stu_id', '')
            major = request.GET.get('major', '')
            userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'time': preach_time}
            save_data_to_database(ticket_id, userdata, 'preach')
            return render(request, 'preach.html', {'result': '很遗憾，这个时间段票抢完了!!', 'name': name, 'code': 0})


class GetVisitTicketView(View):
    """预约参观后台逻辑"""
    def get(self, request):
        times = request.GET.get('times', '')
        ticket_id = r.lpop('V-'+times+'-ticket_id')
        if ticket_id is not None:
            ticket_id = ticket_id.decode('utf8')
            name = request.GET.get('name', '')
            stu_id = request.GET.get('stu_id', '')
            major = request.GET.get('major', '')
            userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'time': times}
            save_data_to_database(ticket_id, userdata, 'visit')
            # 抢票成功应该返回学生的相应信息以及票的信息(包括二维码)以便用于检票
            return render(request, 'visit.html', {'result': ticket_id, 'name': name, 'stu_id': stu_id, 'code': 1, 'times': times})
        else:
            ticket_id = None
            name = request.GET.get('name', '')
            stu_id = request.GET.get('stu_id', '')
            major = request.GET.get('major', '')
            userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'time': times}
            save_data_to_database(ticket_id, userdata, 'visit')
            return render(request, 'visit.html', {'result': '很遗憾，这个时间段票抢完了!!', 'name': name, 'code': 0})


class TicketCheckedView(View):
    """检票系统"""
    def get(self, request):
        if request.user.is_authenticated:       # 判断用户是否登录
            if request.user.is_superuser:       # 判断是否有超级管理员权限
                ticket_id = request.GET.get('ticket_id', '0-0-00000')
                if ticket_id[0] == 'G':
                    user_filter = Grab.objects.filter(ticket_id=ticket_id)
                    if user_filter:
                        user_profile = user_filter.first()
                        if not user_profile.is_checked:
                            name = user_profile.name
                            stu_id = user_profile.stu_id
                            user_profile.is_checked = True
                            user_profile.save()
                            return render(request, 'checked.html', {'result': ticket_id, 'name': name, 'stu_id': stu_id, 'code': 1})
                        else:
                            return render(request, 'checked.html', {'result': '该票已检!!!', 'code': 0})
                    else:
                        return render(request, 'checked.html', {'result': '未查到该票信息!!!', 'code': 0})
                elif ticket_id[0] == 'V':
                    user_filter = VisitTicket.objects.filter(ticket_id=ticket_id)
                    if user_filter:
                        user_profile = user_filter.first()
                        if not user_profile.is_checked:
                            name = user_profile.name
                            stu_id = user_profile.stu_id
                            user_profile.is_checked = True
                            user_profile.save()
                            return render(request, 'checked.html', {'name': name, 'stu_id': stu_id, 'code': 1})
                        else:
                            return render(request, 'checked.html', {'result': '该票已检!!!', 'code': 0})
                    else:
                        return render(request, 'checked.html', {'result': '未查到该票信息!!!', 'code': 0})
            else:
                return render(request, 'checked.html', {'result': '抱歉，您没有权限检票!!!', 'code': 0})
        else:
            return render(request, 'checked.html', {'result': '抱歉，您没有权限检票!!!', 'code': 0})


