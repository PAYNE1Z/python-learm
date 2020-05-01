##### 表结构与数据：
desc department;
# +-------+-------------+------+-----+---------+----------------+
# | Field | Type        | Null | Key | Default | Extra          |
# +-------+-------------+------+-----+---------+----------------+
# | id    | int(11)     | NO   | PRI | NULL    | auto_increment |
# | name  | varchar(20) | YES  |     | NULL    |                |
# +-------+-------------+------+-----+---------+----------------+
# 2 rows in set (0.00 sec)

desc employee;
# +--------+-----------------------+------+-----+---------+----------------+
# | Field  | Type                  | Null | Key | Default | Extra          |
# +--------+-----------------------+------+-----+---------+----------------+
# | id     | int(11)               | NO   | PRI | NULL    | auto_increment |
# | name   | varchar(20)           | YES  |     | NULL    |                |
# | sex    | enum('male','female') | NO   |     | male    |                |
# | age    | int(11)               | NO   |     | NULL    |                |
# | dep_id | int(11)               | YES  |     | NULL    |                |
# +--------+-----------------------+------+-----+---------+----------------+
# 5 rows in set (0.00 sec)

select * from department;
# +----+--------------+
# | id | name         |
# +----+--------------+
# |  1 | 技术         |
# |  2 | 人力资源     |
# |  3 | 销售         |
# |  4 | 运营         |
# +----+--------------+
# 4 rows in set (0.00 sec)

select * from employee;
# +----+------------+--------+-----+--------+
# | id | name       | sex    | age | dep_id |
# +----+------------+--------+-----+--------+
# |  1 | egon       | male   |  18 |      1 |
# |  2 | alex       | female |  48 |      2 |
# |  3 | wupeiqi    | male   |  38 |      2 |
# |  4 | yuanhao    | female |  28 |      5 |
# |  5 | liwenzhou  | male   |  18 |      1 |
# |  6 | jingliyang | female |  18 |      4 |
# +----+------------+--------+-----+--------+
# 6 rows in set (0.00 sec)


### 带IN关键字的子查询
# 1、查询平均年龄在25岁以上的部门名
select name from department where id in (
    select dep_id from employee
        group by dep_id
        having avg(age) > 25
    );
    # +--------------+
    # | name         |
    # +--------------+
    # | 人力资源     |
    # +--------------+
    # 1 row in set (0.00 sec)

# 2、查看技术部员工姓名
select name from employee where dep_id in (
    select id from department
        where name = '技术'
    );
    # +-----------+
    # | name      |
    # +-----------+
    # | egon      |
    # | liwenzhou |
    # +-----------+
    # 2 rows in set (0.00 sec)

# 3、查看不足1人的部门名
select name from department where id not in (   # 那么不在employee表中的部门就是没有人的部门
    select distinct dep_id from employee   # 在employee中的部门都是有人的，去重
    );
    # +--------+
    # | name   |
    # +--------+
    # | 销售   |
    # +--------+
    # 1 row in set (0.00 sec)

### 带比较运算符的子查询
# 1、查询大于所有人平均年龄的员工名与年龄
select name,age from employee where age > (
    select avg(age) from employee
    );
    # +---------+-----+
    # | name    | age |
    # +---------+-----+
    # | alex    |  48 |
    # | wupeiqi |  38 |
    # +---------+-----+
    # 2 rows in set (0.00 sec)

# 2、查询大于部门内平均年龄的员工名、年龄
select t1.dep_id, t1.name, t1.age from employee t1  # 给employee表起个别名 t1
inner join
(select dep_id, avg(age) as avg_age from employee group by dep_id) t2  # 将各部门的平均年龄生成一个新表t2
on t1.dep_id = t2.dep_id   # 将部门id对应的记录连接起来
where t1.age > t2.avg_age;  # 过虑大于各部门

    # +--------+------+-----+
    # | dep_id | name | age |
    # +--------+------+-----+
    # |      2 | alex |  48 |
    # +--------+------+-----+
    # 1 row in set (0.00 sec)

### 带EXISTS关键字的子查询
# department 没有id为5的记录，返回给exists False
select * from employee where exists(select id from department where id=5);
    # Empty set (0.00 sec)

##### 练习： 查询每个部门最新入职的那位员工
# 1、最新入职的就是 hire_date 这个值最大的
# 2、每个部门那就要按部门分组

select t1.name, t1.post, t1.hire_date from db3.employee t1
    inner join
(select post, max(hire_date) as max_hire_date from db3.employee group by post) t2
on t1.post = t2.post
and t1.hire_date = t2.max_hire_date;   # 可以在on这里and多个条件，也可以通过where过虑
# where t1.hire_date = t2.max_hire_date;

    # +--------+-----------------------------------------+------------+
    # | name   | post                                    | hire_date  |
    # +--------+-----------------------------------------+------------+
    # | egon   | 老男孩驻沙河办事处外交大使                | 2017-03-01 |
    # | alex   | teacher                                 | 2015-03-02 |
    # | 格格   | sale                                    | 2017-01-27 |
    # | 张野   | operation                               | 2016-03-11 |
    # +--------+-----------------------------------------+------------+
    # 4 rows in set (0.00 sec)