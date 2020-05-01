# 创建数据库：
create database db2;
use db2;

# 创建用户表：
create table user(
    id int not null unique auto_increment,
    username nvarchar(20) not null,
    password varchar(50) not null
);

# 插入用户信息：
insert into user(username, password) VALUES
('root', password('123456')),
('jack', password('123abc')),
('pony', password('abc123'));


# 创建用户组表：
create table usergroup(
    id int primary key auto_increment,
    groupname varchar(20) not null unique
);

# 插入用户组信息：
insert into usergroup(groupname)
values ('IT'),
       ('Sale'),
       ('Finance'),
       ('Boss');


# 创建主机表：
create table host(
    id int primary key auto_increment,
    ip char(15) not null unique default '127.0.0.1'
);

# 插入主机信息：
insert into host (ip)
values ('192.168.1.120'),
       ('172.16.0.162'),
       ('192.168.0.99'),
       ('172.16.2.138'),
       ('172.16.2.19');


# 创建业务线表:
create table business(
    id int primary key auto_increment,
    business varchar(20) not null unique
);

# 插入业务线信息：
insert into business (business)
values ('支付宝'),
       ('借呗'),
       ('花呗'),
       ('储钱罐');


# 建立user与usergroup关系： 多对一, 多个用户可以在一个组，多个组不能有同一个用户
create table user2usergroup(
    id int not null unique auto_increment,
    user_id int not null,
    group_id int not null,
    primary key (user_id, group_id),
    foreign key (user_id) references user(id),
    foreign key (group_id) references usergroup(id)
);

# 插入用户与组关系信息：
insert into user2usergroup(user_id, group_id)
values (1, 1),
       (2, 4),
       (3, 4);


# 建立user与host关系： 一对一， 一个用户对应一台主机
create table user2host(
    id int not null unique auto_increment,
    user_id int not null,
    host_id int not null,
    primary key(user_id, host_id),
    foreign key(user_id) references user(id),
    foreign key(host_id) references host(id)
);

# 插入用户与主机关系信息：
insert into user2host (user_id, host_id)
values (1, 3),
       (2, 4),
       (3, 5);


# 建立host与business关系： 多对多， 多个主机可以跑一个业务，多个业务可以在一台主机上路
create table host2business(
    id int not null unique auto_increment,
    host_id int not null,
    business_id int not null,
    primary key(host_id, business_id),
    foreign key(host_id) references host(id),
    foreign key(business_id) references business(id)
);

# 插入主机与业务关系信息：
insert into host2business (host_id, business_id)
values (1, 2),
       (2, 3),
       (3, 1),
       (3, 2),
       (3, 3),
       (3, 4),
       (4, 2),
       (4, 3);
