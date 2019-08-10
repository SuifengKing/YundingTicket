from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views import View
# Create your views here.
from get_ticket.models import VisitTicket, Grab
import threading
import redis
import time


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
        return render(request, 'visit.html')


class VisitView(View):
    """参观取票页面"""
    def get(self, request):
        return render(request, 'visit.html')


class GetPreachTicketView(View):
    """抢票后台逻辑"""
    def get(self, request):
        r = redis.StrictRedis()
        all_tickets = r.keys()
        if len(all_tickets) > 0:
            ticket = all_tickets[0]
            ticket_id = r.get(ticket).decode('utf8')
            r.delete(ticket)
            name = request.GET.get('name', '')
            stu_id = request.GET.get('stu_id', '')
            major = request.GET.get('major', '')
            times = request.GET.get('time', '')
            userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'time': times}
            task = threading.Thread(target=save_data_to_database, args=(ticket_id, userdata, 'preach'))
            task.start()
            # 抢票成功应该返回学生的相应信息以及票的信息(包括二维码)以便用于检票
            return render(request, 'visit.html', {'result': ticket_id})
        else:
            ticket_id = None
            name = request.GET.get('name', '')
            stu_id = request.GET.get('stu_id', '')
            major = request.GET.get('major', '')
            times = request.GET.get('time', '')
            userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'time': times}
            task = threading.Thread(target=save_data_to_database, args=(ticket_id, userdata, 'preach'))
            task.start()
            return render(request, 'visit.html', {'result': '很遗憾，票抢完了!!'})


class GetVisitTicketView(View):
    def get(self, request):
        pass


class TicketCheckedView(View):
    """检票系统"""
    def get(self, request):
        if request.user.is_authenticated:       # 判断用户是否登录
            if request.user.is_superuser:       # 判断是否有超级管理员权限
                ticket_id = request.GET.get('ticket_id', '0-00000')
                if ticket_id[0] == 'G':
                    user_filter = Grab.objects.filter(ticket_id=ticket_id)
                    if user_filter:
                        user_profile = user_filter.first()
                        if not user_profile.is_checked:
                            name = user_profile.name
                            major = user_profile.major
                            user_profile.is_checked = True
                            user_profile.save()
                            return HttpResponse('<h1>检票成功!!<br>欢迎您,'+name+'<br>'+major+'<br>'+ticket_id+'</h1>')
                        else:
                            return HttpResponse('<h1>此票已作废!!!</h1>')
                    else:
                        return HttpResponse('<h1>未查到该票信息!!!</h1>')
                elif ticket_id[0] == 'V':
                    pass
            else:
                return HttpResponse('<h1>抱歉，您没有权限检票!!!</h1>')
        else:
            return HttpResponse('<h1>抱歉，您没有权限检票!!!</h1>')


