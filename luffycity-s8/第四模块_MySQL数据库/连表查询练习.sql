##### 准备数据：
# 创建数据库:
create database db4 charset 'utf8';
use db4;

# 创建部门表：
create table department(
    id int not null unique auto_increment,
    name varchar(20)
);

# 插入部门数据：
insert into department (name) values
('技术'),
('人力资源'),
('销售'),
('运营');

# 创建员工表：
create table employee(
    id int primary key auto_increment,
    name varchar(20),
    sex enum('male', 'female') not null default 'male',
    age int not null,
    dep_id int
);

# 插入员工数据：
insert into employee(name,sex,age,dep_id) values
('egon','male',18,1),
('alex','female',48,2),
('wupeiqi','male',38,2),
('yuanhao','female',28,5),
('liwenzhou','male',18,1),
('jingliyang','female',18,4);


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

# employee 表中dep_id为5的数据在 department表中没有对应记录， 而 department表中的id为3的数据在 employee表中也没记录


##### 练习：
# 1 交叉连接：不适用任何匹配条件。生成笛卡尔积
select * from employee,department;
    # +----+------------+--------+-----+--------+----+--------------+
    # | id | name       | sex    | age | dep_id | id | name         |
    # +----+------------+--------+-----+--------+----+--------------+
    # |  1 | egon       | male   |  18 |      1 |  1 | 技术         |
    # |  1 | egon       | male   |  18 |      1 |  2 | 人力资源     |
    # |  1 | egon       | male   |  18 |      1 |  3 | 销售         |
    # |  1 | egon       | male   |  18 |      1 |  4 | 运营         |
    # |  2 | alex       | female |  48 |      2 |  1 | 技术         |
    # |  2 | alex       | female |  48 |      2 |  2 | 人力资源     |
    # |  2 | alex       | female |  48 |      2 |  3 | 销售         |
    # |  2 | alex       | female |  48 |      2 |  4 | 运营         |
    # |  3 | wupeiqi    | male   |  38 |      2 |  1 | 技术         |
    # |  3 | wupeiqi    | male   |  38 |      2 |  2 | 人力资源     |
    # |  3 | wupeiqi    | male   |  38 |      2 |  3 | 销售         |
    # |  3 | wupeiqi    | male   |  38 |      2 |  4 | 运营         |
    # |  4 | yuanhao    | female |  28 |      5 |  1 | 技术         |
    # |  4 | yuanhao    | female |  28 |      5 |  2 | 人力资源     |
    # |  4 | yuanhao    | female |  28 |      5 |  3 | 销售         |
    # |  4 | yuanhao    | female |  28 |      5 |  4 | 运营         |
    # |  5 | liwenzhou  | male   |  18 |      1 |  1 | 技术         |
    # |  5 | liwenzhou  | male   |  18 |      1 |  2 | 人力资源     |
    # |  5 | liwenzhou  | male   |  18 |      1 |  3 | 销售         |
    # |  5 | liwenzhou  | male   |  18 |      1 |  4 | 运营         |
    # |  6 | jingliyang | female |  18 |      4 |  1 | 技术         |
    # |  6 | jingliyang | female |  18 |      4 |  2 | 人力资源     |
    # |  6 | jingliyang | female |  18 |      4 |  3 | 销售         |
    # |  6 | jingliyang | female |  18 |      4 |  4 | 运营         |
    # +----+------------+--------+-----+--------+----+--------------+
    # 24 rows in set (0.00 sec)

# 2 内连接：只连接匹配的行  #找两张表共有的部分，相当于利用条件从笛卡尔积结果中筛选出了正确的结果
select * from employee inner join department on employee.dep_id = department.id;
    # +----+------------+--------+-----+--------+----+--------------+
    # | id | name       | sex    | age | dep_id | id | name         |
    # +----+------------+--------+-----+--------+----+--------------+
    # |  1 | egon       | male   |  18 |      1 |  1 | 技术         |
    # |  2 | alex       | female |  48 |      2 |  2 | 人力资源     |
    # |  3 | wupeiqi    | male   |  38 |      2 |  2 | 人力资源     |
    # |  5 | liwenzhou  | male   |  18 |      1 |  1 | 技术         |
    # |  6 | jingliyang | female |  18 |      4 |  4 | 运营         |
    # +----+------------+--------+-----+--------+----+--------------+
    # 5 rows in set (0.00 sec)

# 3 外链接之左连接：优先显示左表全部记录
# 以左表为准，即找出所有员工信息，当然包括没有部门的员工,没有记录则显示为NULL
# 本质就是：在内连接的基础上增加左边有右边没有的结果
select * from employee left join department on employee.dep_id = department.id;
    # +----+------------+--------+-----+--------+------+--------------+
    # | id | name       | sex    | age | dep_id | id   | name         |
    # +----+------------+--------+-----+--------+------+--------------+
    # |  1 | egon       | male   |  18 |      1 |    1 | 技术         |
    # |  5 | liwenzhou  | male   |  18 |      1 |    1 | 技术         |
    # |  2 | alex       | female |  48 |      2 |    2 | 人力资源     |
    # |  3 | wupeiqi    | male   |  38 |      2 |    2 | 人力资源     |
    # |  6 | jingliyang | female |  18 |      4 |    4 | 运营         |
    # |  4 | yuanhao    | female |  28 |      5 | NULL | NULL         |
    # +----+------------+--------+-----+--------+------+--------------+
    # 6 rows in set (0.00 sec)

# 4 外链接之右连接：优先显示右表全部记录
# 以右表为准，即找出所有部门信息，包括没有员工的部门
# 本质就是：在内连接的基础上增加右边有左边没有的结果
select * from employee right join department on employee.dep_id = department.id;
    # +------+------------+--------+------+--------+----+--------------+
    # | id   | name       | sex    | age  | dep_id | id | name         |
    # +------+------------+--------+------+--------+----+--------------+
    # |    1 | egon       | male   |   18 |      1 |  1 | 技术         |
    # |    2 | alex       | female |   48 |      2 |  2 | 人力资源     |
    # |    3 | wupeiqi    | male   |   38 |      2 |  2 | 人力资源     |
    # |    5 | liwenzhou  | male   |   18 |      1 |  1 | 技术         |
    # |    6 | jingliyang | female |   18 |      4 |  4 | 运营         |
    # | NULL | NULL       | NULL   | NULL |   NULL |  3 | 销售         |
    # +------+------------+--------+------+--------+----+--------------+
    # 6 rows in set (0.00 sec)

# 5 全外连接：显示左右两个表全部记录
# 全外连接：在内连接的基础上增加左边有右边没有的和右边有左边没有的结果
# 注意：mysql不支持全外连接 full JOIN
# 强调：mysql可以使用此种方式间接实现全外连接
select * from employee left join department on employee.dep_id = department.id
union
select * from employee right join department on employee.dep_id = department.id;
    # +------+------------+--------+------+--------+------+--------------+
    # | id   | name       | sex    | age  | dep_id | id   | name         |
    # +------+------------+--------+------+--------+------+--------------+
    # |    1 | egon       | male   |   18 |      1 |    1 | 技术         |
    # |    5 | liwenzhou  | male   |   18 |      1 |    1 | 技术         |
    # |    2 | alex       | female |   48 |      2 |    2 | 人力资源     |
    # |    3 | wupeiqi    | male   |   38 |      2 |    2 | 人力资源     |
    # |    6 | jingliyang | female |   18 |      4 |    4 | 运营         |
    # |    4 | yuanhao    | female |   28 |      5 | NULL | NULL         |
    # | NULL | NULL       | NULL   | NULL |   NULL |    3 | 销售         |
    # +------+------------+--------+------+--------+------+--------------+
    # 7 rows in set (0.04 sec)

# 6、查询各部门的平均年龄;
select department.name, avg(age) from employee inner join department on employee.dep_id = department.id
group by department.name;
    # +--------------+----------+
    # | name         | avg(age) |
    # +--------------+----------+
    # | 人力资源     |  43.0000 |
    # | 技术         |  18.0000 |
    # | 运营         |  18.0000 |
    # +--------------+----------+
    # 3 rows in set (0.02 sec)

# 7、查询平均年龄大于30岁的部门;
select department.name, avg(age) from employee inner join department on employee.dep_id = department.id
group by department.name
having avg(age) > 30;
    # +--------------+----------+
    # | name         | avg(age) |
    # +--------------+----------+
    # | 人力资源     |  43.0000 |
    # +--------------+----------+
    # 1 row in set (0.00 sec)