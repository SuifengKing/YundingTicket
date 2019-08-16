Redis命名规则
可用票以列表形式存储, 表名: G/V-time-tickets
用户抢票信息以哈希(Hash)存储, key: G/V-U-stu_id

requirements:
Django>=2.0
Xadmin==2.0.1
redis
mysqlclient