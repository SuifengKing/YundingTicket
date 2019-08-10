from django.db import models

# Create your models here.


class Grab(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=12)
    stu_id = models.CharField(verbose_name='学号', max_length=10)
    major = models.CharField(verbose_name='专业', max_length=50)
    times = models.CharField(verbose_name='预约时间', max_length=30)
    is_success = models.BooleanField(verbose_name='是否抢票成功', default=False)
    is_checked = models.BooleanField(verbose_name='是否已检票', default=False)
    ticket_id = models.CharField(verbose_name='票号', max_length=15, null=True)


class VisitTicket(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=12)
    stu_id = models.CharField(verbose_name='学号', max_length=10)
    major = models.CharField(verbose_name='专业', max_length=50)
    times = models.CharField(verbose_name='预约时间', max_length=30)
    is_success = models.BooleanField(verbose_name='是否抢票成功', default=False)
    is_checked = models.BooleanField(verbose_name='是否已检票', default=False)
    ticket_id = models.CharField(verbose_name='票号', max_length=15, null=True)
