# 第一模块：开发基础 
## 第一章 Python基础语法 练习题

#### 一、简述编译型与解释型语言的区别，且分别列出你知道的哪些语言属于编译型，哪些属于解释型。
    1.编译型语言是在应用源程序执行之前，就将代码“翻译”成机器码，其目标程序可以脱离其语言环境独立执行，使用比较方便、效率较高。
      属于编译弄语言的有：C、C++等。
    2.解释型语言是在应用源程序执行时，一边由相应语言的解释器“翻译”成机器码一边执行，因此其不能脱离其解释器（语言环境），跨平台性好，效率较低。
      属于解释型语言的有：PHP、Java、Python、Ruby等。


#### 二、执行 Python 脚本的两种方式是什么;
    1. python script.py 调用Python解释器来执行脚本 
    2. ./script.py 直接在命令行执行脚本


#### 三、Python 单行注释和多行注释分别用什么;
    1.单行注释：# 井号放在单行注释语句前
    2.多行注释："""三个双引号包围注释语句""" 或 '''三个双引号包围注释语句'''



#### 四、布尔值分别有什么;
    1.True
    2.False


#### 五、声明变量注意事项有哪些;
    1.变量名只能是字母 数字 下划线的做任意组合
    2.变量名的第一个字符不能是数字
    3.Python自带的一些关键字不声明为变量，如：and or not class print 等


#### 六、如何查看变量在内存中的地址;
    1. 使用id查看变量内存地址: 
       id(variable)
       

#### 补充、 a is b 与  a == b 的区别
```python
# is 是对比两者的内存地址是否一样
# == 是对比两者的值是否一样
a = 257 
b = 257
a is b
# 返回 False
a == b
# 返回 True
```
##### 说明
    Python 解释器对于数字有个小数字缓存池：-5~256， 
    原因是：地址数据最少是32位的，现在都是64位了，如果单独为一个小整数创建一个对象，
    10个地方用到这个小整数，那么就会在内存中创建10个存储的内存地址的空间，
    地址占用的数据长度比数据本身还大这样非常不划算。
    而有这个缓存池，python解释器内部就会共享这个小整数对象，不去开内存空间。
    从而减少内存的使用率，降低浪费。

    字符串也有内存池，给了2k空间，python内部有算法，按照内部权重排列，如果级别高了就把你放入内存。列表、字典都有。


#### 七、写代码：
    需求：
    a. 实现用户输入用户名和密码,当用户名为 seven 且密码为 123 时,显示登陆成功,否则登陆失败；
    b. 实现用户输入用户名和密码,当用户名为 seven 且密码为 123 时,显示登陆成功,否则登陆失败,失败时允许重复输入三次；
    c. 实现用户输入用户名和密码,当用户名为 seven 或 alex 且密码为 123 时,显示登陆成功,否则登陆失败,失败时允许重复输入三次；
  ```python
default_user_list = ["seven", "alex"]
default_pass = "123"
num_of_retries = 3
count = 0
while count < num_of_retries:
    user_name = input("输入用户名：")
    user_pass = input("输入密码：")
    if user_name in default_user_list and user_pass == default_pass:
        print("用户：%s 登录成功!" % user_name)
        break
    else:
        print("用户名或密码输入错误")
    count += 1
else:
    # if count == num_of_retries:
    # 这里两种方式处理三次重试 a. while else  b.在while中用if判断
    print("重试次数超过限制，请稍后再试")
  ```


#### 八、写代码：
    a. 使用while循环实现输出2-3+4-5+6...+100 的和；
  ```python
max_num = 100
count = 2
total = 0
while count <= max_num:
    if count % 2:  # 有余数为真
        total -= count  # 当count为奇数时 total-count 为新的total的值
    else:
        total += count  # 当count为奇数时 total+count 为新的total的值
    count += 1
else:
    print("sum:", total)
  ```

    b. 使用 while 循环实现输出 1,2,3,4,5, 7,8,9, 11,12；
  ```python
n = 1
while n <= 12:
    if n != 6 and n != 10:
        print(n)
    n += 1
```
    c.使用while 循环输出100-50，从大到小，如100，99，98...，到50时再从0循环输出到50，然后结束；
  ``` python
max_num = 10
min_num = 0
break_point = 3
while max_num >= min_num:
    # 从最大值到断点值的循环输出
    print(max_num)
    max_num -= 1
    # 当最大值循环减小到小于断点值 并且 最小值循环加到小于或等于断点值时
    # 执行从最小值到断点值的循环输出
    while max_num < break_point and min_num <= break_point:
        print(min_num)
        min_num += 1
  ```
    d. 使用while 循环实现输出 1-100 内的所有奇数；
  ```python
max_num = 100
min_num = 0
while min_num <= max_num:
    if min_num % 2:
        print(min_num)
    min_num += 1
  ```
    e. 使用 while 循环实现输出 1-100 内的所有偶数；
  ```python
max_num = 100
min_num = 1
while min_num <= max_num:
    if not min_num % 2:
        print(min_num)
    min_num += 1
  ```
  
 ---
 
#### 九、现有如下两个变量,请简述 n1 和 n2 是什么关系：
    n1 = 123456
    n2 = n1
    a. n1和n2指向的是同一个内存地址: 可以用id(n1) id(n2)进行验证


#### 十、制作趣味模板程序（编程题）需求：等待用户输入名字、地点、爱好，根据用户的名字和爱好进行任意显示：如：敬爱可爱的xxx，最喜欢在xxx地方干xxx。
  ```python
user_name = input("请输入你的名字：")
user_local = input("请输入一个地点：")
user_hobby = input("请输入你的爱好：")
print("""
-------------------------------------
# 可爱的%s, 最喜欢在%s, %s
-------------------------------------"""
      % (user_name, user_local, user_hobby))
  ```

---

#### 十一、输入一年份，判断该年份是否是闰年并输出结果。（编程题）注：凡符合下面两个条件之一的年份是闰年。
    a. 能被4整除但不能被100整除；
    b. 能被400整除；
  ```python
years = int(input("请输入一个年份："))
if not years % 400 or (years % 100 and not years % 4):
    print("%s 是闰年" % years)
else:
    print("%s 不是闰年" % years)
  ```

---

#### 十二、假设一年期定期利率为3.25%，计算一下需要过多少年，一万元的一年定期存款连本带息能翻番？（编程题）
  ```python
annual_interest_rate = 0.0325
init_amount = sum_amount = 10000
count = 0
while True:
    count += 1
    sum_amount += init_amount * annual_interest_rate
    print("第%s年: %s" %(count, sum_amount))
    if sum_amount >= init_amount * 2:
        print("想要赚翻番,需要%s年" % count)
        break
  ```

---

#### 十三、使用while,完成以下图形的输出
    *
    * *
    * * *
    * * * *
    * * * * *
    * * * *
    * * *
    * *
    *
  ```python
min_num = count = 0
max_num = 5
while count < max_num:
    count += 1
    print("* " * count)
    while max_num <= count:
        max_num -= 1
        print("* " * max_num)
        if max_num == min_num:
            break
  ```

---

#### 十四、路飞决定根据销售额给员工发提成，提成为阶梯制，假设一个销售人员基本工资为3000元，
    每月业绩低于5万元，无提成；
    5万至10万，提成3%；
    10万至15万提成5%，
    15万-25万提成8%；
    25万至35万提成10%，
    35万以上，提成15%；
    从键盘获取用户当月业绩，计算其工资+提成的总额。
  ```python
base_wage = 3000
performance = int(input("请输入你的业绩: "))
if performance > 350000:
    deduction_wage = performance * 0.15
elif performance > 250000:
    deduction_wage = performance * 0.1
elif performance > 150000:
    deduction_wage = performance * 0.08
elif performance > 100000:
    deduction_wage = performance * 0.05
elif performance > 50000:
    deduction_wage = performance * 0.03
else:
    deduction_wage = performance * 0
print("你的绩效提成为：%s\n总工资为：%s" % (deduction_wage, base_wage + deduction_wage))
  ```

---

#### 十五、北京地铁交通价格调整为：
    6公里(含)内3元;6公里至12公里(含)4元; 12公里至22公里(含)5元；
    22公里至32公里(含)6元;32公里以上部分，每增加1元可乘坐20公里。
    使用市政交通一卡通刷卡乘坐轨道交通，每自然月内每张卡支出累计满100元以后的乘次价格给予8折优惠；
    满150元以后的乘次给予5折优惠，假设每个月，小明都需要上20天班，每次上班需要来回1次，即每天需要乘坐2次同样路线的地铁,编写程序，从键盘获取距离，帮小明计算每月的总花费。
  ```python
ride_count_of_day = 2  # 每天乘坐次数
work_days = 20         # 一个月需要乘坐的天数
ride_count_of_month = ride_count_of_day * work_days   # 一个月需要乘坐的次数
month_way_fare = 0     # 一个月乘坐地铁的总花费
n = 0                  # while循环计数器

mileage = int(input("请输入乘坐地铁的量程(单位公里)："))

# 计算单程车次费用
if mileage > 32:
    # 大于32公里的部分，每20公里加收一元
    # 求出大于32公里的部分，计算有多少个20公里
    over_mileage = mileage - 32
    over_range = over_mileage // 20
    # 超出部分大于20公里的 每乘次为基数6元 + 超出20公里的个数*1元
    if over_range > 0:
        one_way_fare = 6 + over_range * 1
    else:
        one_way_fare = 6 + 1
elif mileage > 22:
    one_way_fare = 6
elif mileage > 12:
    one_way_fare = 5
elif mileage > 6:
    one_way_fare = 4
else:
    one_way_fare = 3

# 循环每次乘车，累计花费
while n < ride_count_of_month:
    # 月累计花费超过150元后的车次，车费5折
    if month_way_fare > 150:
        month_way_fare += one_way_fare * 0.5
    # 月累计花费超过150元后的车次，车费8折
    elif month_way_fare > 100:
        month_way_fare += one_way_fare * 0.8
    # 100元内直接叠加每次乘车费用
    else:
        month_way_fare += one_way_fare
    n += 1
else:
    print("单程里程：%s , 每月需要：%.2f元" % (mileage, month_way_fare))
  ```
  
---

#### 十六、一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在第10次落地时，共经过多少米？第10次反弹多高？
  ```python
height = total_height = 100  # 球的初始高度与总行程高度（因为是是高处落下，所以总行程的始值跟初始高度一致)
rebound_count = 10           # 回弹次数
n = 0                        # 计数器

# 循环计算总行程与第10次回弹高度
while n < rebound_count:
    height *= 0.5               # 每次回弹高度为前一次的一半
    total_height += height * 2  # 总行程等于前面的总和 + 当前次回弹高度*2 (回弹还要落下，所以要*2)
    n += 1
else:
    print("球10次落地后共经过：%.2f米，第10次反弹高度为：%.2f米" % (total_height, height))

  ```

---

