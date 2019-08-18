Redis命名规则
可用票以列表形式存储, 表名: G/V-time-tickets
用户抢票信息以哈希(Hash)存储, key: G/V-U-stu_id

requirements:
Django>=2.0
Xadmin==2.0.1
redis
mysqlclient

V0.0
完成了大体架构;
……;

V1.0
把直接数据库存储改为Redis;

V1.5
完成了admin对Redis里余票以及抢票信息的统一管理;
修改了一些小细节;

V1.5.1
精简了一些冗余代码;
把页面逻辑与设计稿改为一致形式;
增加了404和500页面的处理;


以后可能要解决的问题:
在重置余票处不应该使用flushall;
进一步精简代码, 优化逻辑;
可能还得有宣讲人信息的增加;

