from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
# Create your views here.
from get_ticket.models import VisitTicket, Grab
import redis
import time

all_times_dict = {
    '1': '12:30 PM',
    '2': '19:00 PM',
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


def save_data_to_database(redis_conn, ticket_id, userdata, ticket_type):
    """把数据存入到Redis数据库"""
    stu_id = userdata.get('stu_id', '')
    if ticket_id is not None:
        userdata['ticket_id'] = ticket_id
        userdata['is_success'] = 1
    userdata['times'] = all_times_dict.get(userdata.get('times', '0'))
    if ticket_type == 'visit':
        redis_conn.hmset('V-U-'+stu_id, userdata)
    elif ticket_type == 'preach':
        redis_conn.hmset('G-U-'+stu_id, userdata)


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
        return render(request, 'visit.html', {'result': '', 'times_dict': visit_times_dict})


class GetPreachTicketView(View):
    """抢票后台逻辑"""
    def post(self, request):
        r = redis.StrictRedis(decode_responses=True)
        times = request.POST.get('times', '')
        ticket_id = r.lpop('G-'+times+'-tickets')
        name = request.POST.get('name', '')
        stu_id = request.POST.get('stu_id', '')
        major = request.POST.get('major', '')
        userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'times': times}
        save_data_to_database(r, ticket_id, userdata, 'preach')
        if ticket_id is not None:
            # 抢票成功应该返回学生的相应信息以及票的信息(包括二维码)以便用于检票
            return render(request, 'successful_preach.html', {'name': name, 'stu_id': stu_id})
        else:
            return render(request, 'fail.html')


class GetVisitTicketView(View):
    """预约参观后台逻辑"""
    def post(self, request):
        r = redis.StrictRedis(decode_responses=True)
        times = request.POST.get('times', '')
        ticket_id = r.lpop('V-'+times+'-tickets')
        name = request.POST.get('name', '')
        stu_id = request.POST.get('stu_id', '')
        major = request.POST.get('major', '')
        userdata = {'name': name, 'stu_id': stu_id, 'major': major, 'times': times}
        save_data_to_database(r, ticket_id, userdata, 'visit')
        if ticket_id is not None:
            # 抢票成功应该返回学生的相应信息以及票的信息(包括二维码)以便用于检票
            return render(request, 'successful_visit.html', {'name': name, 'stu_id': stu_id})
        else:
            return render(request, 'fail.html')


class ExportTicketView(View):
    def post(self, request):
        stu_id = request.POST.get('stu_id', '')
        ticket_type = request.POST.get('type', '')
        r = redis.StrictRedis(decode_responses=True)
        is_success = r.hget(ticket_type+'-U-'+stu_id, 'is_success')
        if is_success:
            stu_info = r.hgetall(ticket_type + '-U-' + stu_id)
            if ticket_type == 'G':
                return render(request, 'ticket_preach.html', stu_info)
            elif ticket_type == 'V':
                return render(request, 'ticket_visit.html', stu_info)
        else:
            # 查询MySQL
            if ticket_type == 'G':
                user_filter = Grab.objects.filter(stu_id=stu_id, is_success=True)
                if user_filter:
                    user_profile = user_filter.first()
                    name = user_profile.name
                    ticket_id = user_profile.ticket_id
                    times = user_profile.times
                    return render(request, 'ticket_preach.html', {'name': name, 'ticket_id': ticket_id, 'times': times})
                else:
                    return render(request, 'fail.html')
            elif ticket_type == 'V':
                user_filter = VisitTicket.objects.filter(stu_id=stu_id, is_success=True)
                if user_filter:
                    user_profile = user_filter.first()
                    name = user_profile.name
                    ticket_id = user_profile.ticket_id
                    times = user_profile.times
                    return render(request, 'ticket_visit.html', {'name': name, 'ticket_id': ticket_id, 'times': times})
                else:
                    return render(request, 'fail.html')


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


def page_not_found(request, exception):
    """404状态的处理"""
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    """500状态的处理"""
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response

