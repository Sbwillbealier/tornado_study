CREATE DATABASE `ihome` DEFAULT CHARACTER SET utf8;

use ihome;

CREATE TABLE ih_user_info (
    ui_user_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    ui_name varchar(32) NOT NULL COMMENT '昵称',
    ui_mobile char(11) NOT NULL COMMENT '手机号',
    ui_passwd varchar(64) NOT NULL COMMENT '密码',
    ui_real_name varchar(32) NULL COMMENT '真实姓名',
    ui_id_card varchar(20) NULL COMMENT '身份证号',
    ui_avatar varchar(128) NULL COMMENT '用户头像',
    ui_admin tinyint NOT NULL DEFAULT '0' COMMENT '是否是管理员，0-不是，1-是',
    ui_utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
    ui_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (ui_user_id),
    UNIQUE (ui_name),
    UNIQUE (ui_mobile)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COMMENT='用户信息表';

create table ih_house_info(
    hi_house_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '房屋id',
    hi_user_id bigint unsigned NOT NULL COMMENT '用户ID',
    hi_title varchar(64) NOT NULL COMMENT '房屋名称',
    hi_address varchar(512) NOT NULL DEFAULT '' COMMENT '地址',
    hi_price int unsigned NOT NULL DEFAULT '0' COMMENT '房屋价格，单位分',
    hi_utime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
    hi_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (hi_house_id),
    CONSTRAINT FOREIGN KEY (`hi_user_id`) REFERENCES `ih_user_info` (`ui_user_id`)
)engine=InnoDB default charset=utf8 comment '房屋信息表';

CREATE TABLE ih_house_image (
    hi_image_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '图片id',
    hi_house_id bigint unsigned NOT NULL COMMENT '房屋id',
    hi_url varchar(256) NOT NULL COMMENT '图片url',
    hi_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (hi_image_id),
    CONSTRAINT FOREIGN KEY (hi_house_id) REFERENCES ih_house_info (hi_house_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='房屋图片表';