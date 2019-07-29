CREATE TABLE `bug_logs`(
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT 'bug记录id',
    `count` INT NOT NULL COMMENT '第几次执行',
    `test_case_id` INT NOT NULL COMMENT '测试用例id',
    `request_url` VARCHAR ( 255 ) NOT NULL COMMENT '请求url',
    `method` VARCHAR ( 255 ) NOT NULL COMMENT '请求方法',
    `expect_result` VARCHAR ( 255 ) NOT NULL COMMENT '预期结果',
    `response` VARCHAR ( 255 ) NOT NULL COMMENT '响应',
    `result` VARCHAR ( 255 ) NOT NULL COMMENT '实际结果',
    `create_at` DATETIME NOT NULL COMMENT '记录时间'
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT 'bug记录表';