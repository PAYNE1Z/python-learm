
--2、查询学生总人数；
select count(sid) from student;


-- 3、查询“生物”课程和“物理”课程成绩都及格的学生id和姓名；
-- a. 在course表拿到两门课程的cid,
-- b. 通过cid在score表拿到score >= 60的学生ID，并统计过虑出现两次的学生student_id
-- c. 通过student_id在student表找出学生sid与sname
select
    sid, sname
from student where sid in (
    select
        student_id
    from scor where course_id in (
        select cid from course where cname in ('物理'))
        and score >= 60
        group by student_id
        having count(student_id) = 2
    );

	
-- 4、查询每个年级的班级数，取出班级数最多的前三个年级；
-- a. 在class表中按grade_id分组排序取出最多的前三个
-- b. 与class_grade表连接并取年级名称，id,与班级数
-- 注: 由于子查询中使用了limit所有无法再使用where in 来找到年级，所以使用内连接
select t1.gid, t1.gname, t2.count_cls from class_grade as t1
inner join
(select grade_id,count(grade_id) as count_cls from class
    group by grade_id
    order by count_cls desc
    limit 3) as t2
on t1.gid = t2.grade_id
order by t2.count_cls desc;


-- 5、查询平均成绩最高和最低的学生的id和姓名以及平均成绩；
-- a. 在score表统计各学员课程的平均分数
-- b. 分别取出平均分最高与最小的学生student_id与score
-- c. 全表连接两个结果集，最显示标题
SELECT 
	'最高平均分' as 'result',
	(SELECT sname FROM student WHERE sid = t1.student_id) as student_name,
	t1.max_score as score
FROM (
	SELECT student_id, avg(score) as max_score 
	FROM score 
	GROUP BY student_id
	ORDER BY avg(score) DESC LIMIT 1
	) t1
UNION
SELECT 
	'最低平均分',
	(SELECT sname FROM student WHERE sid = t2.student_id) as student_name,
	t2.min_score as score
FROM (
	SELECT student_id, avg(score) as min_score 
	FROM score 
	GROUP BY student_id
	ORDER BY avg(score) LIMIT 1
	) t2;
	

-- 6、查询每个年级的学生人数；
-- a. 在student表统计学生所在班级学生数
-- b. 将a的结果与class表连接为c
-- c. 在c表统计学生所在年级与学生数连接到class_grade表
-- d. 通过gid,gname查询到年级ID与年级名称及年级学员人数
select gid,gname,d.grade_students from class_grade
INNER JOIN
	(select c.grade_id,sum(student_num) as grade_students
		from
			(select b.grade_id,a.student_num from class b
			INNER JOIN
				(select class_id,count(sid) as student_num from student
			GROUP BY class_id) a
			ON a.class_id = b.cid) c
GROUP BY grade_id) d
ON gid = d.grade_id;


-- 7、查询每位学生的学号，姓名，选课数，平均成绩；
-- a. 在score表统计学生选课数与平均成绩与student连接
-- b. 查询相关字段
SELECT sid,sname,s2.course_num,s2.avg_score from student s1
INNER JOIN
	(select student_id, count(course_id) as course_num, avg(score) as avg_score
	from score
	GROUP BY student_id) s2
ON s1.sid = s2.student_id;


-- 8、查询学生编号为“2”的学生的姓名、该学生成绩最高的课程名、成绩最低的课程名及分数；
-- a. 在score表中查出最高分与最低分的课程cid与course表连接
-- b. 通过cid在course表中取到课程名称与studentd表连接
SELECT sname, t3.cname, t3.score
	FROM student
INNER JOIN
	(SELECT cname,t2.score FROM course t1
	INNER JOIN
        (SELECT course_id,score
            FROM score
            WHERE student_id = '2'
            AND score = (select max(score) from score where student_id = '2')
            OR score = (select min(score) from score where student_id = '2')
            ) t2
	ON t1.cid = t2.course_id) t3
WHERE sid = '2';


-- 9、查询姓“李”的老师的个数和所带班级数；
-- a. 查询并统计李姓老师个数
-- b. 与teach2cls表连接统计老师所带班级数
SELECT t2.teacher_li_num, count(t1.cid) as class_num
	FROM teach2cls t1
INNER JOIN
	(SELECT count(tid) as teacher_li_num,tid
		FROM teacher
		WHERE tname like '李%') t2
ON t1.tid = t2.tid
GROUP BY t1.tid;


-- 10、查询班级数小于5的年级id和年级名；
-- a. 在class表中查询并统计年级所属的班级数，并过滤班级数小于5的
-- b. 与class_grade表连接查询年级ID与名称
SELECT t1.gid, t1.gname
	FROM class_grade t1
INNER JOIN
	(SELECT grade_id, count(cid) as class_num
		FROM class
		GROUP BY grade_id
		HAVING class_num < 5) t2
ON t1.gid = t2.grade_id;


-- 11、查询班级信息，包括班级id、班级名称、年级、年级级别(12为低年级，34为中年级，56为高年级)，示例结果
-- a. 连表class，class_grade查询，并匹配
SELECT
	cid as '班级ID',
	caption as '班级名称',
	gname as '年级',
	CASE WHEN LEFT(gname, 1) IN ('一','二') THEN '低'
	     WHEN LEFT(gname, 1) IN ('三','四') THEN '中'
			 ELSE '高'
	END as '年级级别'
	FROM class
INNER JOIN
	class_grade
ON class.grade_id = class_grade.gid;


-- 12、查询学过“张三”老师2门课以上的同学的学号、姓名；
-- a. 在teacher表查到张三老师的tid
-- b. 通过tid在course表找到张三老师的课程cid
-- c. 通过cid在score表中统计每个学员张三老师课程的数量，并过滤2门及以上的学员
SELECT sid, sname
	FROM student
INNER JOIN
	(SELECT student_id, count(course_id) as course_num
		FROM score WHERE course_id in (
			SELECT cid FROM course WHERE teacher_id = (
				SELECT tid FROM teacher WHERE tname = '张三'
				)
		)
		GROUP BY student_id
		HAVING count(course_id) >= 2
	) t1
ON student.sid = t1.student_id;


-- 13、查询教授课程超过2门的老师的id和姓名；
-- a. 在course表中统计各老师课程数据，并过滤多于2门课程的老师
-- b. 连表teacher查询姓名与id
SELECT tid, tname
	FROM teacher
INNER JOIN
	(SELECT teacher_id,count(cid) as course_num
		FROM course
		GROUP BY teacher_id
		HAVING count(cid) > 2
	) t1
ON teacher.tid = t1.teacher_id


-- 14、查询学过编号“1”课程和编号“2”课程的同学的学号、姓名；
SELECT sid,sname
	FROM student
	WHERE sid in (
		SELECT student_id
			FROM score
			WHERE course_id in (1,2)
	)

	
-- 15、查询没有带过高年级的老师id和姓名；
-- a. 在class表中查出高年级班级cid
-- b. 通过cid在teach2cls表中查出有带高年级班级的老师tid
-- c. 连表teacher过滤出没有带过高年级的老师id与姓名
SELECT teacher.tid, tname 
	FROM teacher
INNER JOIN
	(SELECT tid FROM teach2cls
		WHERE cid in (
			SELECT cid FROM class
				WHERE LEFT(caption, 1) in ('五','六','七','八'))
	) t1
ON teacher.tid != t1.tid;


-- 16、查询学过“张三”老师所教的所有课的同学的学号、姓名；
-- a. 在teacher表中找到张三tid
-- b. 通过tid在course表找到张三所有课程cid
-- c. 统计张三课程数据,找到上了所有张三课程的学生
SELECT sid, sname 
	FROM student
INNER JOIN
	(SELECT student_id, count(course_id) as courses
		FROM score
		WHERE course_id in (
			(SELECT cid FROM course
				WHERE teacher_id = (SELECT tid FROM teacher WHERE tname = '张三'))
		)
		GROUP BY student_id
		HAVING count(course_id) = (
			select count(cid) FROM course 
				WHERE teacher_id = (SELECT tid FROM teacher WHERE tname = '张三'))
	) t1
ON t1.student_id = sid;


-- 17、查询带过超过2个班级的老师的id和姓名；
-- a. 在teach2cls表中统计各老师班级，并过滤多于2个班级的老师
-- b. 连表teacher查询姓名与id
SELECT teacher.tid, tname
	FROM teacher
INNER JOIN
	(SELECT tid,count(cid) as class_num
		FROM teach2cls
		GROUP BY tid
		HAVING count(cid) > 2
	) t1
ON teacher.tid = t1.tid


-- 18、查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名；
-- a. 在score表中找到同时学了编号为1与2的学生sid,并过滤2课程比1课程分低的
SELECT sid,sname
	FROM student
	WHERE sid in (
		SELECT t1.student_id
			FROM score as t1 
		INNER JOIN 
			score as t2
		ON t1.student_id = t2.student_id AND t1.course_id = 1 AND t2.course_id = 2
		WHERE t1.score < t2.score
	);
	

-- 19、查询所带班级数最多的老师id和姓名；
-- a. 在teach2cls表中统计各老师班级，并排序找出最多班级的老师
-- b. 连表teacher查询姓名与id
SELECT teacher.tid, tname
	FROM teacher
INNER JOIN
	(SELECT tid,count(cid) as class_num
		FROM teach2cls
		GROUP BY tid
		ORDER BY count(cid) DESC
		limit 1
	) t1
ON teacher.tid = t1.tid;


-- 20、查询所有课程成绩小于60分的同学的学号、姓名；
-- a. 统计所有学员课程数
-- b. 统计各学员少于60分的课程数
-- c. 过滤小于60分课程数等于总课程数的学员ID、姓名
SELECT sid, sname
	FROM student
INNER JOIN
	(SELECT t1.student_id, count(t1.course_id) as course_num, t3.fail_course
		FROM score t1
	INNER JOIN
		(SELECT t2.student_id,count(t2.course_id) as fail_course
			FROM score t2
			WHERE score < 60
			GROUP BY t2.student_id
		) t3
	ON t1.student_id = t3.student_id
	GROUP BY t1.student_id
	) t4
ON student.sid = t4.student_id AND t4.course_num = t4.fail_course;


-- 21、查询没有学全所有课的同学的学号、姓名；
-- a. 统计课程总数
-- b. 统计各学员所学课程数
-- c. 过滤学员所学课程数等于总课程数的学生
SELECT sid, sname
	FROM student
	WHERE sid in (
		SELECT student_id
			FROM score
			GROUP BY student_id
			HAVING count(course_id) = (SELECT count(cid) FROM course)
	);
	

-- 22、查询至少有一门课与学号为“1”的同学所学相同的同学的学号和姓名；
-- a. 查找学号1学生的所有课程
-- b. 查找有学习学号1学生课程的学生去重
SELECT sid, sname
	FROM student
	WHERE sid in (
		SELECT DISTINCT student_id 
			FROM score 
			WHERE course_id in (SELECT course_id FROM score WHERE student_id = 1)
	);


-- 23、查询至少学过学号为“1”同学所选课程中任意一门课的其他同学学号和姓名；
-- a. 查找学号1学生的所有课程
-- b. 查找有学习学号1学生课程的学生去重
SELECT sid, sname
	FROM student
	WHERE sid in (
		SELECT DISTINCT student_id 
			FROM score 
			WHERE course_id in (SELECT course_id FROM score WHERE student_id = 1)
	) AND sid != 1;
	

-- 24、查询和“2”号同学学习的课程完全相同的其他同学的学号和姓名；
-- a. 查找学号2学生的所有课程
-- b. 与score表连接，过滤跟2号学生课程id一样的学生ID与课程ID与一样的课程数量same_course_num
-- c. 再与各学员所有课程数量total_course_num 结果连接
-- d. 通过b步骤的过滤出有相同数量一样课程的学员：
-- 		如学员2有 1,6两门课程，学员3有 1,6,7三门课程，课程总数不一样，但一样的课程数量是一样的 
-- 		所有，需要再过滤一次，必须与2号学员的总课程数也是一样的
SELECT sid, sname
	FROM student
	WHERE sid in (SELECT t4.student_id
		FROM (SELECT student_id, same_course_num
			FROM (SELECT student_id, count(t1.course_id) as same_course_num
					FROM score t1
				INNER JOIN
					(SELECT course_id
						FROM score 
						WHERE student_id=2
					) t2
				WHERE t1.course_id = t2.course_id AND t1.student_id !=2
				GROUP BY t1.student_id
				HAVING count(t1.course_id) = (SELECT count(course_id) FROM score WHERE student_id=2)	
			) t3
		) t4
	INNER JOIN
		(SELECT student_id, count(course_id) as total_course_num
			FROM score
			GROUP BY student_id
			HAVING count(course_id) = (SELECT count(course_id) FROM score WHERE student_id=2) 
		) t5
	ON t5.student_id = t4.student_id AND t4.same_course_num = t5.total_course_num
	);
	
	
-- 25、删除学习“张三”老师课的score表记录；
-- a. 在teacher表找到张三老师tid
-- b. 通过tid在course表找到张三老师的课程cid
-- c. 在socre表删除
DELETE 
FROM 
	score 
WHERE 
	course_id in ( SELECT cid FROM course 
		WHERE teacher_id = (SELECT tid FROM teacher WHERE tname='张三')
);

	
-- 26、向score表中插入一些记录，这些记录要求符合以下条件：①没有上过编号“2”课程的同学学号；②插入“2”号课程的平均成绩；
-- a. 在score表中找出上2号课程的学员id,再从student表中取出没有上过的学员ID
-- b. 统计2号课程所有学生的平均成绩
INSERT INTO 
	score(student_id, course_id, score)
SELECT t1.sid, 2, t2.avg_score
	FROM ( 
		(SELECT sid FROM student 
			WHERE sid NOT IN (SELECT student_id FROM score WHERE course_id = 2)) t1,
		(SELECT avg(score) as avg_score FROM score WHERE course_id = 2) t2
	);


-- 27、按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示： 
-- 学生ID,语文, 数学,英语,课程数和平均分；
-- a. 不管有没有学 ‘语文‘， ‘数学’，‘英语’ 这三门课程都要显示成绩，没有就显示空
-- b. 统计各学生的报读课程数量，与课程平均分
SELECT 
	student_id,
	(SELECT score FROM score 
		WHERE course_id = (SELECT cid FROM course WHERE cname='语文') AND score.student_id =s1.student_id ) AS '语文',
	(SELECT score FROM score 
		WHERE course_id = (SELECT cid FROM course WHERE cname='数学') AND score.student_id =s1.student_id ) AS '数学',
	(SELECT score FROM score 
		WHERE course_id = (SELECT cid FROM course WHERE cname='英语') AND score.student_id =s1.student_id ) AS '英语',
	count(course_id) AS '课程数',
	avg(score) AS '平均分'
FROM score as s1
GROUP BY student_id
ORDER BY avg(score);


-- 28、查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分；
-- a. 在score表中统计各课程的id，最高分与最低分
-- b. 与course连接，显示所有课程学生报名情况
SELECT 
	cid AS '课程ID', t1.max_score AS '最高分', t1.min_score AS '最低分'
FROM 
	(SELECT 
		course_id, max(score) AS max_score, min(score) AS min_score 
	FROM score
	GROUP BY course_id) t1
RIGHT JOIN 
	course
ON cid = t1.course_id;


-- 29、按各科平均成绩从低到高和及格率的百分数从高到低顺序；
-- a. 大于等于60分为及格，及格数/总课程数*100 = 及格率
SELECT
	course_id,
	avg(score) AS avg_score,
	sum(CASE WHEN score.score >= 60 THEN 1 ELSE 0 END) / count(sid) * 100 AS pass_percent
FROM score
GROUP BY course_id
ORDER BY avg(score) ASC, pass_percent DESC;


-- 30、课程平均分从高到低显示（现实任课老师）；
-- a. 找出所有老师对应课程
-- b. 统计并排序
SELECT t2.cid, t2.cname, t2.tname, t3.avg_score
FROM (SELECT tid, tname, cid, cname
	FROM teacher t1
	INNER JOIN
		course s1
	ON t1.tid = s1.teacher_id
	)AS t2
INNER JOIN
   (SELECT course_id,avg(score)as avg_score 
	FROM score GROUP BY course_id 
	)AS t3
ON t2.cid=t3.course_id
ORDER BY avg_score DESC;


-- 31、查询各科成绩前三名的记录(不考虑成绩并列情况) ；
-- a. 通过子查询在两个score表中过滤出各course_id的分数前三取出来
-- b. （不考虑并列，就要给score去重）, 按course_id排序再按score倒序
SELECT DISTINCT score, course_id
FROM score t1 
WHERE ( 
	SELECT count(sid) 
	FROM score 
	WHERE course_id = t1.course_id AND t1.score < score
	) < 3 
ORDER BY course_id, score DESC;


-- 32、查询每门课程被选修的学生数；
-- a. 在score表中统计各课程报名学生数量
-- b. 与course连接，显示所有课程学生报名情况
SELECT 
	cid,cname,t1.studend_num 
FROM 
	(SELECT course_id, count(student_id) as studend_num FROM score GROUP BY course_id) t1
RIGHT JOIN 
	course
ON t1.course_id = cid
ORDER BY cid;


-- 33、查询选修了2门以上课程的全部学生的学号和姓名；
-- a. 在score表中统计各学员选课数量
-- b. 过滤2门以上的学员
SELECT t1.student_id, sname
FROM student
INNER JOIN
	(SELECT student_id, count(course_id) as course_num FROM score GROUP BY student_id) t1
ON t1.student_id = sid
WHERE t1.course_num >= 2;


-- 34、查询男生、女生的人数，按倒序排列；
SELECT gender, count(sid) as gender_num
FROM student
GROUP BY gender
ORDER BY count(sid) DESC;


-- 35、查询姓“张”的学生名单；
SELECT * FROM student WHERE LEFT(sname,1) = '张';


-- 36、查询同名同姓学生名单，并统计同名人数；
SELECT sname, count(sid)
FROM student
GROUP BY sname
HAVING count(sid)>1;


-- 37、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列；
-- a. 在score表中统计各课程平均成绩
-- b. 与course连接，显示所有课程成绩并排序
SELECT 
	cid,cname,t1.avg_score 
FROM 
	(SELECT course_id, avg(score) as avg_score FROM score GROUP BY course_id) t1
RIGHT JOIN 
	course
ON t1.course_id = cid
ORDER BY avg_score, cid DESC;


-- 38、查询课程名称为“数学”，且分数低于60的学生姓名和分数；
-- a. 在score表中查出数学课程且分数低于60的学生student_id与score
-- b. 与student连表查出学生姓名
SELECT t1.student_id,sname,t1.score
FROM student
INNER JOIN
	(SELECT student_id, score  
		FROM score 
		WHERE course_id = (SELECT cid FROM course WHERE cname = '数学') AND score < 60
	) t1
ON t1.student_id = sid


-- 39、查询课程编号为“3”且课程成绩在80分以上的学生的学号和姓名；
SELECT t1.student_id,sname,t1.score
FROM student
INNER JOIN
	(SELECT student_id, score  
		FROM score 
		WHERE course_id = 3 AND score > 80
	) t1
ON t1.student_id = sid


-- 40、求选修了课程的学生人数
SELECT count(1) as choice_course_stu_num
FROM (SELECT DISTINCT student_id FROM score) t1


-- 41、查询选修“王五”老师所授课程的学生中，成绩最高和最低的学生姓名及其成绩；
-- a. 在course表中找出王五老师所授课程cid
-- b. 在score表中找出王五老师课程的最高分与最低分的学生ID与分数
-- c. 全连接最高与最低成绩结果，并国上标题 
SELECT 
	'成绩最高' as 'result',
	(SELECT sname FROM student WHERE sid = t1.student_id) as student_name,
	t1.score
FROM (
	SELECT student_id, max(score) as score
	FROM score 
	WHERE course_id in (
		SELECT cid FROM course WHERE teacher_id = (SELECT tid FROM teacher WHERE tname = '王五')
		)
	) t1
UNION
SELECT 
	'成绩最低',
	(SELECT sname FROM student WHERE sid = t2.student_id) as student_name,
	t2.score 
FROM (
	SELECT student_id, min(score) as score
	FROM score 
	WHERE course_id in (
		SELECT cid FROM course WHERE teacher_id = (SELECT tid FROM teacher WHERE tname = '王五')
		)
	) t2;


-- 42、查询各个课程及相应的选修人数；
-- a. 在score表中统计各课程选修学生数量
-- b. 与course连接，显示所有课程学生选修情况
SELECT 
	cid,cname,t1.studend_num 
FROM 
	(SELECT course_id, count(student_id) as studend_num FROM score GROUP BY course_id) t1
RIGHT JOIN 
	course
ON t1.course_id = cid
ORDER BY cid;


--43、查询不同课程但成绩相同的学生的学号、课程号、学生成绩；
-- a. 有多个字段使用distinct去重时是所有字段都一样
-- b. 解决方法使用 min,max 与group by 处理去重字段，
SELECT 
	s1.course_id as CourseIdA,
	min(s2.course_id) as CourseIdB,
	s1.student_id as StudentIdA,
	s2.student_id as StudentIdB,
	s1.score as ScoreA,
	s2.score as ScoreB
FROM
	score as s1,
	score as s2
WHERE 
	s1.score = s2.score AND s1.course_id != s2.course_id
GROUP BY s1.course_id


--44、查询每门课程成绩最好的前两名学生id和姓名；
-- a. 通过子查询在两个score表中过滤出各course_id的分数前二取出来
-- b. 按course_id排序再按score倒序
SELECT sid, sname, t2.course_id, t2.score
FROM student
INNER JOIN
	(SELECT DISTINCT score, course_id, student_id
	FROM score t1 
	WHERE ( 
		SELECT count(sid) 
		FROM score 
		WHERE course_id = t1.course_id AND t1.score < score
		) < 2
	) t2
ON sid = t2.student_id
ORDER BY t2.course_id, t2.score DESC;


--45、检索至少选修两门课程的学生学号；
-- a. 在score表中统计各学员选课数量
-- b. 过滤2门以上的学员
SELECT t1.student_id
FROM student
INNER JOIN
	(SELECT student_id, count(course_id) as course_num FROM score GROUP BY student_id) t1
ON t1.student_id = sid
WHERE t1.course_num >= 2;


--46、查询没有学生选修的课程的课程号和课程名；
-- a. 在score分组查找出有学生报选的课程ID
-- b. 在course表中过滤出没有学生报选的课程
SELECT cid, cname 
FROM course
WHERE cid not in (SELECT course_id FROM score GROUP BY course_id)；


--47、查询没带过任何班级的老师id和姓名；
-- a. 在teach2clse中查找有学生报选的老师tid
-- b. 在teacher表中过滤出没有班级的老师
SELECT tid, tname
FROM teacher
WHERE tid not in (SELECT DISTINCT tid FROM teach2cls)


-- 48、查询有两门以上课程超过80分的学生id及其平均成绩；
-- a.在score表中统计出80分以上的课程，分组统计各学员80分以上的课程数量及课程平均分数，并过滤有2门以上的
-- b.连接student表查询学生信息
SELECT sid, sname, t1.avg_score
FROM student
INNER JOIN
	(SELECT 
		student_id, count(course_id) as course_num, avg(score) as avg_score 
	FROM score 
	WHERE score > 80 
	GROUP BY student_id 
	HAVING count(course_id) >= 2) t1
ON t1.student_id = sid


-- 49、检索“3”课程分数小于60，按分数降序排列的同学学号；
SELECT student_id, score
FROM score 
WHERE course_id = 3 AND score < 60
ORDER BY score DESC;


-- 50、删除编号为“2”的同学的“1”课程的成绩；
DELETE FROM score WHERE student_id = 2 AND course_id = 1;


-- 51、查询同时选修了物理课和生物课的学生id和姓名；
-- a. 在course表中找出物理与生物课的cid
-- b. 通过cid在score表中统计有报这两门课程的学生，分组统计每个学员针对这两门课程的数据，并过滤等于2门的学员
SELECT sid, sname
FROM student
WHERE sid in (
	SELECT student_id
	FROM score 
	WHERE course_id in (SELECT cid FROM course WHERE cname in ('物理','生物'))
	GROUP BY student_id
	HAVING count(course_id) = 2
	);