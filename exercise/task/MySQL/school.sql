/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50724
Source Host           : localhost:3306
Source Database       : school

Target Server Type    : MYSQL
Target Server Version : 50724
File Encoding         : 65001

Date: 2019-08-16 10:59:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `class`
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `caption` char(20) NOT NULL,
  `grade_id` int(11) NOT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `caption` (`caption`),
  KEY `grade_id` (`grade_id`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `class_grade` (`gid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of class
-- ----------------------------
INSERT INTO `class` VALUES ('1', '一年一班', '1');
INSERT INTO `class` VALUES ('2', '二年一班', '2');
INSERT INTO `class` VALUES ('3', '二年二班', '2');
INSERT INTO `class` VALUES ('4', '二年三班', '2');
INSERT INTO `class` VALUES ('5', '三年一班', '3');
INSERT INTO `class` VALUES ('6', '三年二班', '3');
INSERT INTO `class` VALUES ('7', '四年一班', '4');
INSERT INTO `class` VALUES ('8', '四年二班', '4');
INSERT INTO `class` VALUES ('9', '五年一班', '5');

-- ----------------------------
-- Table structure for `class_grade`
-- ----------------------------
DROP TABLE IF EXISTS `class_grade`;
CREATE TABLE `class_grade` (
  `gid` int(11) NOT NULL AUTO_INCREMENT,
  `gname` char(20) NOT NULL,
  PRIMARY KEY (`gid`),
  UNIQUE KEY `gname` (`gname`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of class_grade
-- ----------------------------
INSERT INTO `class_grade` VALUES ('1', '一年级');
INSERT INTO `class_grade` VALUES ('3', '三年级');
INSERT INTO `class_grade` VALUES ('2', '二年级');
INSERT INTO `class_grade` VALUES ('5', '五年级');
INSERT INTO `class_grade` VALUES ('4', '四年级');

-- ----------------------------
-- Table structure for `course`
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `cname` char(20) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  PRIMARY KEY (`cid`),
  UNIQUE KEY `cname` (`cname`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`tid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('1', '生物', '1');
INSERT INTO `course` VALUES ('2', '体育', '2');
INSERT INTO `course` VALUES ('3', '音乐', '3');
INSERT INTO `course` VALUES ('4', '美术', '3');
INSERT INTO `course` VALUES ('5', '武术', '2');
INSERT INTO `course` VALUES ('6', '物理', '4');
INSERT INTO `course` VALUES ('7', '数学', '5');
INSERT INTO `course` VALUES ('8', '语文', '6');
INSERT INTO `course` VALUES ('9', '化学', '1');

-- ----------------------------
-- Table structure for `score`
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  UNIQUE KEY `sid` (`sid`),
  KEY `student_id` (`student_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `score_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of score
-- ----------------------------
INSERT INTO `score` VALUES ('1', '1', '1', '68');
INSERT INTO `score` VALUES ('2', '1', '6', '81');
INSERT INTO `score` VALUES ('3', '1', '7', '39');
INSERT INTO `score` VALUES ('4', '2', '6', '73');
INSERT INTO `score` VALUES ('5', '2', '9', '81');
INSERT INTO `score` VALUES ('6', '2', '1', '63');
INSERT INTO `score` VALUES ('7', '3', '7', '98');
INSERT INTO `score` VALUES ('8', '3', '4', '88');
INSERT INTO `score` VALUES ('9', '3', '3', '26');
INSERT INTO `score` VALUES ('10', '4', '4', '64');
INSERT INTO `score` VALUES ('11', '4', '5', '90');
INSERT INTO `score` VALUES ('12', '4', '9', '72');
INSERT INTO `score` VALUES ('13', '5', '1', '72');
INSERT INTO `score` VALUES ('14', '5', '5', '100');
INSERT INTO `score` VALUES ('15', '5', '6', '96');
INSERT INTO `score` VALUES ('16', '6', '8', '100');
INSERT INTO `score` VALUES ('17', '6', '2', '100');
INSERT INTO `score` VALUES ('18', '7', '2', '83');
INSERT INTO `score` VALUES ('19', '7', '3', '91');
INSERT INTO `score` VALUES ('20', '8', '5', '80');
INSERT INTO `score` VALUES ('21', '9', '8', '73');
INSERT INTO `score` VALUES ('22', '9', '6', '64');
INSERT INTO `score` VALUES ('23', '10', '2', '50');
INSERT INTO `score` VALUES ('24', '10', '3', '77');
INSERT INTO `score` VALUES ('25', '11', '1', '68');
INSERT INTO `score` VALUES ('26', '11', '7', '49');
INSERT INTO `score` VALUES ('27', '11', '8', '87');
INSERT INTO `score` VALUES ('28', '12', '3', '66');
INSERT INTO `score` VALUES ('29', '12', '2', '77');
INSERT INTO `score` VALUES ('30', '12', '4', '83');
INSERT INTO `score` VALUES ('31', '12', '9', '60');

-- ----------------------------
-- Table structure for `student`
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` char(20) NOT NULL,
  `gender` enum('男','女') NOT NULL,
  `class_id` int(11) NOT NULL,
  PRIMARY KEY (`sid`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('1', '马云', '男', '1');
INSERT INTO `student` VALUES ('2', '马化腾', '男', '1');
INSERT INTO `student` VALUES ('3', '李彦宏', '男', '5');
INSERT INTO `student` VALUES ('4', '周杰伦', '男', '3');
INSERT INTO `student` VALUES ('5', '周星驰', '男', '4');
INSERT INTO `student` VALUES ('6', '成龙', '男', '5');
INSERT INTO `student` VALUES ('7', '李连杰', '男', '6');
INSERT INTO `student` VALUES ('8', '潘韦柏', '男', '7');
INSERT INTO `student` VALUES ('9', '王力宏', '男', '8');
INSERT INTO `student` VALUES ('10', '蔡依林', '女', '3');
INSERT INTO `student` VALUES ('11', '迪丽热巴', '女', '2');
INSERT INTO `student` VALUES ('12', '董明珠', '女', '2');

-- ----------------------------
-- Table structure for `teach2cls`
-- ----------------------------
DROP TABLE IF EXISTS `teach2cls`;
CREATE TABLE `teach2cls` (
  `tcid` int(11) NOT NULL AUTO_INCREMENT,
  `tid` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  UNIQUE KEY `tcid` (`tcid`),
  KEY `tid` (`tid`),
  KEY `cid` (`cid`),
  CONSTRAINT `teach2cls_ibfk_1` FOREIGN KEY (`tid`) REFERENCES `teacher` (`tid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `teach2cls_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `class` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teach2cls
-- ----------------------------
INSERT INTO `teach2cls` VALUES ('1', '1', '1');
INSERT INTO `teach2cls` VALUES ('2', '1', '2');
INSERT INTO `teach2cls` VALUES ('3', '2', '5');
INSERT INTO `teach2cls` VALUES ('4', '2', '3');
INSERT INTO `teach2cls` VALUES ('5', '3', '1');
INSERT INTO `teach2cls` VALUES ('6', '4', '7');
INSERT INTO `teach2cls` VALUES ('7', '5', '9');
INSERT INTO `teach2cls` VALUES ('8', '5', '6');
INSERT INTO `teach2cls` VALUES ('9', '6', '1');
INSERT INTO `teach2cls` VALUES ('10', '2', '3');

-- ----------------------------
-- Table structure for `teacher`
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `tname` char(20) NOT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('1', '张三');
INSERT INTO `teacher` VALUES ('2', '李四');
INSERT INTO `teacher` VALUES ('3', '王五');
INSERT INTO `teacher` VALUES ('4', '赵六');
INSERT INTO `teacher` VALUES ('5', '钱七');
INSERT INTO `teacher` VALUES ('6', '周八');
