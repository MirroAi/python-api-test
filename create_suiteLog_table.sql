/*
* @Author: MirrorAi
* @Date:   2019-08-17 20:21:05
* @Last Modified by:   MirroAi
* @Last Modified time: 2019-08-17 20:24:21
*/

CREATE TABLE `suite logs`(
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志id',
    `count` INT NOT NULL COMMENT '第几次执行',
    `suite_id` INT NOT NULL COMMENT '测试套件id',
    `suite_name` VARCHAR ( 255 ) NOT NULL COMMENT '套件名',
    `interface_name` VARCHAR ( 255 ) NOT NULL COMMENT '接口名',
    `is_success` INT NOT NULL COMMENT '是否成功，成功 1，失败 0',
    `create_at` DATETIME NOT NULL COMMENT '记录时间'
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT '套件执行日志表';