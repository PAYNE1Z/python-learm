# 创建数据库：
create database db3;
use db3;


# 创建班级表：
create table class(
    id int not null unique auto_increment,
    caption varchar(20) not null unique
);

# 插入班级数据：
insert into class (caption)
values ('一年二班'),
       ('一年三班'),
       ('二年二班'),
       ('三年二班');


# 创建学生表：  关联class表中的id  多对一，多个学生可以在一个班级，但一个学生不能在多个班级
create table student(
    id int not null unique auto_increment,
    sname char(15) not null,
    gender enum('男', '女') default '男',
    class_id int not null,
    foreign key(class_id) references class(id)
);

# 插入学生数据:
insert into student (sname, gender, class_id)
values ('陈一', '女', 4),
       ('林二', '女', 2);

insert into student (sname, class_id)
values ('张三', 3),
       ('李四', 1),
       ('王五', 1),
       ('赵六', 4),
       ('何七', 1),
       ('周八', 4);


# 创建老师表：
create table teacher(
    id int primary key auto_increment,
    tname char(20) not null
);

# 插入老师数据：
insert into teacher (tname)
values ('波多野结衣'),
       ('苍井空'),
       ('饭岛爱'),
       ('吉泽玛丽亚');


# 创建课程表： 关联老师表， 多对一， 一个老师可以上多门课程，但一门课程不能多个老师上
create table course (
    id int primary key auto_increment,
    cname char(10) not null,
    teacher_id int not null,
    foreign key(teacher_id) references teacher(id)
);

# 插入课程数据：
insert into course (cname, teacher_id) VALUES
('生物', 1),
('体育', 1),
('物理', 3),
('日语', 4),
('瑜伽', 2);


# 创建成绩表：关联学生与课程， 多对多， 一个学生有多门课程，一门课程有多个学生
create table score(
    id int not null unique auto_increment,
    student_id int not null,
    course_id int not null,
    score int not null,
    foreign key(student_id) references student(id),
    foreign key(course_id) references course(id)
);

# 插入成绩数据：
insert into score (student_id, course_id, score) VALUES
(1, 1, 99),
(1, 2, 100),
(1, 4, 38),
(2, 3, 98),
(2, 2, 89),
(2, 4, 60),
(3, 1, 55),
(3, 2, 78),
(3, 3, 100),
(3, 4, 100),
(4, 1, 18),
(4, 4, 90);

