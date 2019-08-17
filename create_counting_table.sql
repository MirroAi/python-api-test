CREATE TABLE `counting`(
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    `type` INT NOT NULL COMMENT '类型，区分执行单个用例还是执行测试套件',
    `count` INT DEFAULT 0 COMMENT '计数，用于记录第几次执行'
)ENGINE=INNODB CHARSET=utf8mb4 COMMENT '计数表';