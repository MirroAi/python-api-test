CREATE TABLE `test_case_suite` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
    `suite_name` VARCHAR ( 255 ) NOT NULL COMMENT '套件名',
    `interface_name` VARCHAR ( 255 ) NOT NULL COMMENT '接口名称',
    `host` VARCHAR(255) NOT NULL COMMENT '接口域名',
    `url` VARCHAR ( 255 ) NOT NULL COMMENT '接口url地址',
    `method` VARCHAR ( 255 ) NOT NULL COMMENT '请求方法',
    `param` VARCHAR ( 255 ) COMMENT '请求参数',
    `body` VARCHAR ( 255 ) COMMENT '请求体',
    `expect_result` VARCHAR ( 255 ) NOT NULL COMMENT '预期结果',
    `commit` VARCHAR ( 255 ) COMMENT '备注'
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT '测试套件表';