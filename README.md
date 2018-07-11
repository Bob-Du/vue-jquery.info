信息管理系统
===

通过一个web页面 连接后台程序 实现了对数据库中信息的增删改查

数据库为 db.bobdu.cc root账号 密码123456


数据库初始化代码为:

```
create database info_db default charset = utf8;

use info_db;

create table info (
    id int unsigned not null auto_increment primary key,
    name varchar(32) not null,
    sex tinyint unsigned,
    age tinyint unsigned,
    email varchar(32)
) engine = innodb default charset = utf8;

INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (1, '老大', 1, 22, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (2, '老二', 0, 21, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (3, '张三', 1, 12, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (4, '李四', 0, 33, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (5, '王五', 0, 24, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (6, '赵六', 0, 42, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (7, '周七', 1, 11, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (8, '吴八', 1, 17, '123@123.com');
INSERT INTO `info_copy1`(`id`, `name`, `sex`, `age`, `email`) VALUES (9, '郑九', 1, 42, '123@123.com');


```