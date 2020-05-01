-- 1、创建存储过程实例(有参)

# 参数有三类：
# IN 输入参数：表示调用者向过程传入值（传入值可以是字面量或变量）
# OUT 输出参数：表示过程向调用者传出值(可以返回多个值)（传出值只能是变量）
# INOUT 输入输出参数：既表示调用者向过程传入值，又表示过程向调用者传出值（值只能是变量）

delimiter //  			
create procedure p2(
	in n1 char(20),   		-- 参数格式：类型 参数 数据类型
	in n2 char(20)
)   
BEGIN					-- 开始
	select * from user;
	insert into user(name, password) values
	(n1, md5(n2));      -- 使用参数
END //					
delimiter ;				


-- 2、查看存储过程;
show create procedure p2;


-- 3、存储过程调用方式
---- a. 在MySQL中：
call p2('joshua', '123456')   -- 有参数记得传参

---- b. 在Python中基于pymysql:
cursor.callproc('p2', ('joshua', '123456'))  -- 参数放元袓中
print(cursor.fetchall())


