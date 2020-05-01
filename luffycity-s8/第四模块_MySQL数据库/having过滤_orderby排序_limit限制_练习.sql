##### 示例数据
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

# 表数据：
# mysql> select * from employee;
# +----+------------+--------+-----+------------+-----------------------------------------+--------------+------------+--------+-----------+
# | id | name       | sex    | age | hire_date  | post                                    | post_comment | salary     | office | depart_id |
# +----+------------+--------+-----+------------+-----------------------------------------+--------------+------------+--------+-----------+
# |  1 | egon       | male   |  18 | 2017-03-01 | 老男孩驻沙河办事处外交大使              | NULL         |    7300.33 |    401 |         1 |
# |  2 | alex       | male   |  78 | 2015-03-02 | teacher                                 | NULL         | 1000000.31 |    401 |         1 |
# |  3 | wupeiqi    | male   |  81 | 2013-03-05 | teacher                                 | NULL         |    8300.00 |    401 |         1 |
# |  4 | yuanhao    | male   |  73 | 2014-07-01 | teacher                                 | NULL         |    3500.00 |    401 |         1 |
# |  5 | liwenzhou  | male   |  28 | 2012-11-01 | teacher                                 | NULL         |    2100.00 |    401 |         1 |
# |  6 | jingliyang | female |  18 | 2011-02-11 | teacher                                 | NULL         |    9000.00 |    401 |         1 |
# |  7 | jinxin     | male   |  18 | 1900-03-01 | teacher                                 | NULL         |   30000.00 |    401 |         1 |
# |  8 | 成龙       | male   |  48 | 2010-11-11 | teacher                                 | NULL         |   10000.00 |    401 |         1 |
# |  9 | 歪歪       | female |  48 | 2015-03-11 | sale                                    | NULL         |    3000.13 |    402 |         2 |
# | 10 | 丫丫       | female |  38 | 2010-11-01 | sale                                    | NULL         |    2000.35 |    402 |         2 |
# | 11 | 丁丁       | female |  18 | 2011-03-12 | sale                                    | NULL         |    1000.37 |    402 |         2 |
# | 12 | 星星       | female |  18 | 2016-05-13 | sale                                    | NULL         |    3000.29 |    402 |         2 |
# | 13 | 格格       | female |  28 | 2017-01-27 | sale                                    | NULL         |    4000.33 |    402 |         2 |
# | 14 | 张野       | male   |  28 | 2016-03-11 | operation                               | NULL         |   10000.13 |    403 |         3 |
# | 15 | 程咬金     | male   |  18 | 1997-03-12 | operation                               | NULL         |   20000.00 |    403 |         3 |
# | 16 | 程咬银     | female |  18 | 2013-03-11 | operation                               | NULL         |   19000.00 |    403 |         3 |
# | 17 | 程咬铜     | male   |  18 | 2015-04-11 | operation                               | NULL         |   18000.00 |    403 |         3 |
# | 18 | 程咬铁     | female |  18 | 2014-05-12 | operation                               | NULL         |   17000.00 |    403 |         3 |
# +----+------------+--------+-----+------------+-----------------------------------------+--------------+------------+--------+-----------+
# 18 rows in set (0.00 sec)


# HAVING与WHERE不一样的地方在于!!!!!!
#！！！执行优先级从高到低：where > group by > having
#1. Where 发生在分组group by之前，因而Where中可以有任意字段，但是绝对不能使用聚合函数。
#2. Having发生在分组group by之后，因而Having中可以使用分组的字段，无法直接取到其他字段,可以使用聚合函数


##### having 练习：
# 1. 查询各岗位内包含的员工个数小于2的岗位名、岗位内包含员工名字、个数
select post, group_concat(name), count(id) from employee group by post having count(id) > 2;
    # +-----------+---------------------------------------------------------+-----------+
    # | post      | group_concat(name)                                      | count(id) |
    # +-----------+---------------------------------------------------------+-----------+
    # | operation | 张野,程咬金,程咬银,程咬铜,程咬铁                        |         5 |
    # | sale      | 歪歪,丫丫,丁丁,星星,格格                                |         5 |
    # | teacher   | alex,wupeiqi,yuanhao,liwenzhou,jingliyang,jinxin,成龙   |         7 |
    # +-----------+---------------------------------------------------------+-----------+
    # 3 rows in set (0.00 sec)

# 3. 查询各岗位平均薪资大于10000的岗位名、平均工资
select post, avg(salary) from employee group by post having avg(salary) > 10000;
    # +-----------+---------------+
    # | post      | avg(salary)   |
    # +-----------+---------------+
    # | operation |  16800.026000 |
    # | teacher   | 151842.901429 |
    # +-----------+---------------+
    # 2 rows in set (0.00 sec)

# 4. 查询各岗位平均薪资大于10000且小于20000的岗位名、平均工资
select post, avg(salary) from employee group by post having avg(salary) between 10000 and 20000;
    # +-----------+--------------+
    # | post      | avg(salary)  |
    # +-----------+--------------+
    # | operation | 16800.026000 |
    # +-----------+--------------+
    # 1 row in set (0.00 sec)


##### order by 练习：
# 1. 查询所有员工信息，先按照age升序排序，如果age相同则按照hire_date降序排序
select * from employee order by age, hire_date desc;
    # +----+------------+--------+-----+------------+-----------------------------------------+--------------+------------+--------+-----------+
    # | id | name       | sex    | age | hire_date  | post                                    | post_comment | salary     | office | depart_id |
    # +----+------------+--------+-----+------------+-----------------------------------------+--------------+------------+--------+-----------+
    # |  1 | egon       | male   |  18 | 2017-03-01 | 老男孩驻沙河办事处外交大使              | NULL         |    7300.33 |    401 |         1 |
    # | 12 | 星星       | female |  18 | 2016-05-13 | sale                                    | NULL         |    3000.29 |    402 |         2 |
    # | 17 | 程咬铜     | male   |  18 | 2015-04-11 | operation                               | NULL         |   18000.00 |    403 |         3 |
    # | 18 | 程咬铁     | female |  18 | 2014-05-12 | operation                               | NULL         |   17000.00 |    403 |         3 |
    # | 16 | 程咬银     | female |  18 | 2013-03-11 | operation                               | NULL         |   19000.00 |    403 |         3 |
    # | 11 | 丁丁       | female |  18 | 2011-03-12 | sale                                    | NULL         |    1000.37 |    402 |         2 |
    # |  6 | jingliyang | female |  18 | 2011-02-11 | teacher                                 | NULL         |    9000.00 |    401 |         1 |
    # | 15 | 程咬金     | male   |  18 | 1997-03-12 | operation                               | NULL         |   20000.00 |    403 |         3 |
    # |  7 | jinxin     | male   |  18 | 1900-03-01 | teacher                                 | NULL         |   30000.00 |    401 |         1 |
    # | 13 | 格格       | female |  28 | 2017-01-27 | sale                                    | NULL         |    4000.33 |    402 |         2 |
    # | 14 | 张野       | male   |  28 | 2016-03-11 | operation                               | NULL         |   10000.13 |    403 |         3 |
    # |  5 | liwenzhou  | male   |  28 | 2012-11-01 | teacher                                 | NULL         |    2100.00 |    401 |         1 |
    # | 10 | 丫丫       | female |  38 | 2010-11-01 | sale                                    | NULL         |    2000.35 |    402 |         2 |
    # |  9 | 歪歪       | female |  48 | 2015-03-11 | sale                                    | NULL         |    3000.13 |    402 |         2 |
    # |  8 | 成龙       | male   |  48 | 2010-11-11 | teacher                                 | NULL         |   10000.00 |    401 |         1 |
    # |  4 | yuanhao    | male   |  73 | 2014-07-01 | teacher                                 | NULL         |    3500.00 |    401 |         1 |
    # |  2 | alex       | male   |  78 | 2015-03-02 | teacher                                 | NULL         | 1000000.31 |    401 |         1 |
    # |  3 | wupeiqi    | male   |  81 | 2013-03-05 | teacher                                 | NULL         |    8300.00 |    401 |         1 |
    # +----+------------+--------+-----+------------+-----------------------------------------+--------------+------------+--------+-----------+
    # 18 rows in set (0.00 sec)

# 2. 查询各岗位平均薪资大于10000的岗位名、平均工资,结果按平均薪资升序排列
select post,avg(salary) as avg_salary from employee group by post having avg(salary) > 10000 order by avg_salary;
    # 因为order by会在select后执行，所有order by这里可以使用avg_salary
    # +-----------+---------------+
    # | post      | avg_salary    |
    # +-----------+---------------+
    # | operation |  16800.026000 |
    # | teacher   | 151842.901429 |
    # +-----------+---------------+
    # 2 rows in set (0.00 sec)

# 3. 查询各岗位平均薪资大于10000的岗位名、平均工资,结果按平均薪资降序排列
select post,avg(salary) as avg_salary from employee group by post having avg(salary) > 10000 order by avg_salary desc;
    # +-----------+---------------+
    # | post      | avg_salary    |
    # +-----------+---------------+
    # | teacher   | 151842.901429 |
    # | operation |  16800.026000 |
    # +-----------+---------------+
    # 2 rows in set (0.00 sec)


##### limit 练习：
# 1. 分页显示，每页5条
SELECT * from employee limit 0,5;
SELECT * from employee limit 10,5;
SELECT * from employee limit 15,5;
