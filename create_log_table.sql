CREATE TABLE `logs`(
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志id',
    `count` INT NOT NULL COMMENT '第几次执行',
    `test_case_id` INT NOT NULL COMMENT '测试用例id',
    `is_success` INT NOT NULL COMMENT '是否成功，成功 1，失败 0'
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT '执行日志表';