# company.employee
#     员工id      id                  int
#     姓名        emp_name            varchar
#     性别        sex                 enum
#     年龄        age                 int
#     入职日期     hire_date           date
#     岗位        post                varchar
#     职位描述     post_comment        varchar
#     薪水        salary              double
#     办公室       office              int
#     部门编号     depart_id           int

#创建表
create table employee(
    id int not null unique auto_increment,
    name varchar(20) not null,
    sex enum('male','female') not null default 'male',  # 大部分是男的
    age int(3) unsigned not null default 28,
    hire_date date not null,
    post varchar(50),
    post_comment varchar(100),
    salary double(15,2),
    office int,         # 一个部门一个办公室
    depart_id int
);

# 表结构：
# mysql> desc employee;
# +--------------+-----------------------+------+-----+---------+----------------+
# | Field        | Type                  | Null | Key | Default | Extra          |
# +--------------+-----------------------+------+-----+---------+----------------+
# | id           | int(11)               | NO   | PRI | NULL    | auto_increment |
# | name         | varchar(20)           | NO   |     | NULL    |                |
# | sex          | enum('male','female') | NO   |     | male    |                |
# | age          | int(3) unsigned       | NO   |     | 28      |                |
# | hire_date    | date                  | NO   |     | NULL    |                |
# | post         | varchar(50)           | YES  |     | NULL    |                |
# | post_comment | varchar(100)          | YES  |     | NULL    |                |
# | salary       | double(15,2)          | YES  |     | NULL    |                |
# | office       | int(11)               | YES  |     | NULL    |                |
# | depart_id    | int(11)               | YES  |     | NULL    |                |
# +--------------+-----------------------+------+-----+---------+----------------+

#插入记录
#三个部门：教学，销售，运营
# ps：如果在windows系统中，插入中文字符，select的结果为空白，可以将所有字符编码统一设置成gbk
insert into employee(name,sex,age,hire_date,post,salary,office,depart_id) values
('egon','male',18,'20170301','老男孩驻沙河办事处外交大使',7300.33,401,1),  # 以下是教学部
('alex','male',78,'20150302','teacher',1000000.31,401,1),
('wupeiqi','male',81,'20130305','teacher',8300,401,1),
('yuanhao','male',73,'20140701','teacher',3500,401,1),
('liwenzhou','male',28,'20121101','teacher',2100,401,1),
('jingliyang','female',18,'20110211','teacher',9000,401,1),
('jinxin','male',18,'19000301','teacher',30000,401,1),
('成龙','male',48,'20101111','teacher',10000,401,1),
('歪歪','female',48,'20150311','sale',3000.13,402,2),  # 以下是销售部门
('丫丫','female',38,'20101101','sale',2000.35,402,2),
('丁丁','female',18,'20110312','sale',1000.37,402,2),
('星星','female',18,'20160513','sale',3000.29,402,2),
('格格','female',28,'20170127','sale',4000.33,402,2),
('张野','male',28,'20160311','operation',10000.13,403,3),  # 以下是运营部门
('程咬金','male',18,'19970312','operation',20000,403,3),
('程咬银','female',18,'20130311','operation',19000,403,3),
('程咬铜','male',18,'20150411','operation',18000,403,3),
('程咬铁','female',18,'20140512','operation',17000,403,3)
;


##### 查询练习：
# 1. 查看岗位是teacher的员工姓名、年龄
select name,age from employee where post='teacher';
    # +------------+-----+
    # | name       | age |
    # +------------+-----+
    # | alex       |  78 |
    # | wupeiqi    |  81 |
    # | yuanhao    |  73 |
    # | liwenzhou  |  28 |
    # | jingliyang |  18 |
    # | jinxin     |  18 |
    # | 成龙       |  48 |
    # +------------+-----+

# 2. 查看岗位是teacher且年龄大于30岁的员工姓名、年龄
select name, age from employee where post='teacher' and age > 30;
    # +---------+-----+
    # | name    | age |
    # +---------+-----+
    # | alex    |  78 |
    # | wupeiqi |  81 |
    # | yuanhao |  73 |
    # | 成龙    |  48 |
    # +---------+-----+
    # 4 rows in set (0.00 sec)

# 3. 查看岗位是teacher且薪资在9000-10000范围内的员工姓名、年龄、薪资
select name, age, salary from employee where post='teacher' and salary between 9000 and 10000;
    # +------------+-----+----------+
    # | name       | age | salary   |
    # +------------+-----+----------+
    # | jingliyang |  18 |  9000.00 |
    # | 成龙       |  48 | 10000.00 |
    # +------------+-----+----------+
    # 2 rows in set (0.00 sec)

# 4. 查看岗位描述不为NULL的员工信息
select * from employee where post_comment is not null;
    # Empty set (0.00 sec)

# 5. 查看岗位是teacher且薪资是10000或9000或30000的员工姓名、年龄、薪资
select name, age, salary from employee where post='teacher' and  salary in (10000, 9000, 30000);
    # +------------+-----+----------+
    # | name       | age | salary   |
    # +------------+-----+----------+
    # | jingliyang |  18 |  9000.00 |
    # | jinxin     |  18 | 30000.00 |
    # | 成龙       |  48 | 10000.00 |
    # +------------+-----+----------+
    # 3 rows in set (0.00 sec)

# 6. 查看岗位是teacher且薪资不是10000或9000或30000的员工姓名、年龄、薪资
select name, age, salary from employee where post='teacher' and salary not in (10000, 9000, 30000);
    # +-----------+-----+------------+
    # | name      | age | salary     |
    # +-----------+-----+------------+
    # | alex      |  78 | 1000000.31 |
    # | wupeiqi   |  81 |    8300.00 |
    # | yuanhao   |  73 |    3500.00 |
    # | liwenzhou |  28 |    2100.00 |
    # +-----------+-----+------------+
    # 4 rows in set (0.00 sec)

# 7. 查看岗位是teacher且名字是jin开头的员工姓名、年薪
select name, salary*12 as annual_salary from employee where post='teacher' and name like 'jin%';
    # +------------+---------------+
    # | name       | annual_salary |
    # +------------+---------------+
    # | jingliyang |     108000.00 |
    # | jinxin     |     360000.00 |
    # +------------+---------------+
    # 2 rows in set (0.00 sec)