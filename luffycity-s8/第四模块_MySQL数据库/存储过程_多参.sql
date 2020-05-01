
-- 1、创建一个查询用户密码的存储过程

delimiter //
create procedure get_user_pass(
	in u_name char(20),  -- 接收用户名
	out u_pass char(32)  -- 返回用户密码
)
BEGIN
	declare u_pass char(32) default '';  -- 必须先定义要返回值的变量,如果这里不定义,在调用前需要定义
	set u_pass = (select password from user where name = u_name)
END //
delimiter ;


-- 2、查看存储过程;
show create procedure get_user_pass;


-- 3、存储过程调用方式
---- a. 在MySQL中：必须先定义一个要接收返回值的变量
call p2('joshua', @u_pass)   -- 返回值必须是变量, @u_pass就是返回值
select @u_pass               -- 查看返回值  

---- b. 在Python中基于pymysql:
cursor.callproc('p2', ('joshua', ''))  -- 传入参数第二个参数为'' 就相当于 set @u_pass = '' (必须要传)
print(cursor.fetchall())

cursor.exceute('select @_get_user_pass_0, @_get_user_pass_1')  -- 查询返回值 @_get_user_pass_0代表第一个参数是传入的值，@_get_user_pass_1代表第二个参数，即返回值
print(cursor.fetchall()) 

