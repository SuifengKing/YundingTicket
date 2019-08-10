# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 17:02
# @Author  : Yaojie Chang
# @File    : urls.py
# @Software: PyCharm

from django.urls import path
from get_ticket.views import PreachView, VisitView, GetPreachTicketView, GetVisitTicketView, TicketCheckedView

urlpatterns = [
    path('preach/', PreachView.as_view(), name='preach'),
    path('visit/', VisitView.as_view(), name='visit'),
    path('get_preach_ticket/', GetPreachTicketView.as_view(), name='get_preach_ticket'),
    path('get_visit_ticket/', GetVisitTicketView.as_view(), name='get_visit_ticket'),
    path('ticket_checked/', TicketCheckedView.as_view(), name='ticket_checked'),
]
