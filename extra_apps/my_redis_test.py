import redis
import random
import time
import MySQLdb

r = redis.StrictRedis()


def add_preach_ticket(num=[('1', 20), ('2', 20)]):
    start_time = time.time()
    for times in num:
        for key in range(times[1]):
            all_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
            active_code = ''
            for i in range(5):
                active_code += random.choice(all_char)
            # r.set('G-'+times[0]+'-ticket'+str(key), 'G-'+times[0]+'-'+active_code)
            # r.set('G-'+times[0]+'-'+active_code, '1')
            r.lpush('G-'+times[0]+'-ticket_id', 'G-'+times[0]+'-'+active_code)

    r.save()
    end_time = time.time()

    print('Redis写数据:', end_time-start_time)


def add_visit_ticket(num=[]):
    start_time = time.time()
    for times in num:
        for key in range(times[1]):
            all_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
            active_code = ''
            for i in range(5):
                active_code += random.choice(all_char)
            r.set('V-'+times[0]+'-ticket'+str(key), 'V-'+times[0]+'-'+active_code)

    r.save()
    end_time = time.time()

    print('Redis写数据:', end_time-start_time)


def delete_all():
    start_time = time.time()
    while True:
        all_keys = r.keys()
        if len(all_keys) > 0:
            key = random.choice(all_keys)
            r.delete(key)
        else:
            break
    all_keys = r.keys()
    end_time = time.time()

    print('Redis读取并删除:', end_time-start_time)


def pop_all():
    start_time = time.time()
    ticket_id = r.lpop('ticket_id')
    while ticket_id is not None:
        ticket_id = r.lpop('ticket_id')
    end_time = time.time()

    print('Redis列表弹出:', end_time-start_time)


add_preach_ticket(num=[('1', 20), ('2', 20)])
# add_visit_ticket(num=[('8', 5),
#                       ('10', 5),
#                       ('12', 5),
#                       ('13', 5),
#                       ('14', 5),
#                       ('16', 5),
#                       ('18', 5),
#                       ('19', 5),
#                       ('20', 5),
#                       ('21', 5),])
# pop_all()

# delete_all()
