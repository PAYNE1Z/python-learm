-- 1、创建存储过程实例(无参)

delimiter //  			-- 声明结束符为//
create procedure p1()   -- 创建名为p1的存储过程	
BEGIN					-- 开始
	select * from user; -- 要执行的SQL语句
	insert into user(name, password) values
	('payne', md5('123456'));
END //					-- 结束
delimiter ;				-- 恢复结束符为;


-- 2、查看存储过程;
show create procedure p1;


-- 3、存储过程调用方式
---- a. 在MySQL中：
call p1()

---- b. 在Python中基于pymysql:
cursor.callproc('p1')
print(cursor.fetchall())


