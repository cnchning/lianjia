/*
Navicat MySQL Data Transfer

Source Server         : 菲多
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : lianjia

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-12-18 09:34:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for avgDistrict
-- ----------------------------
DROP TABLE IF EXISTS `avgDistrict`;
CREATE TABLE `avgDistrict` (
  `ymd` int(10) NOT NULL DEFAULT 20181213 COMMENT '年月日： yyyymmdd',
  `district` varchar(20) NOT NULL COMMENT '行政区名字',
  `bedroom_num` tinyint(4) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL COMMENT '平均单价',
  `total_price` decimal(10,2) NOT NULL COMMENT '平均总价',
  `build_area` decimal(10,2) NOT NULL COMMENT '平均建筑面积',
  `inside_area` decimal(10,2) NOT NULL COMMENT '平均套内面积',
  `num_house` smallint(6) NOT NULL COMMENT '在线房子套数',
  `follow` decimal(10,2) NOT NULL COMMENT '平均关注，热度',
  `take_look` decimal(10,2) NOT NULL COMMENT '平均带看，热度',
  PRIMARY KEY (`ymd`,`district`,`bedroom_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for avgEstate
-- ----------------------------
DROP TABLE IF EXISTS `avgEstate`;
CREATE TABLE `avgEstate` (
  `ymd` int(10) NOT NULL DEFAULT 20181213 COMMENT '年月日： yyyymmdd',
  `housing_estate` varchar(20) NOT NULL COMMENT '小区名字',
  `bedroom_num` tinyint(4) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL COMMENT '平均单价',
  `total_price` decimal(10,2) NOT NULL COMMENT '平均总价',
  `build_area` decimal(10,2) NOT NULL COMMENT '平均建筑面积',
  `inside_area` decimal(10,2) NOT NULL COMMENT '平均套内面积',
  `num_house` smallint(6) NOT NULL COMMENT '在线房子套数',
  `follow` decimal(10,2) NOT NULL COMMENT '平均关注，热度',
  `take_look` decimal(10,2) NOT NULL COMMENT '平均带看，热度',
  PRIMARY KEY (`ymd`,`housing_estate`,`bedroom_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for avgPosition
-- ----------------------------
DROP TABLE IF EXISTS `avgPosition`;
CREATE TABLE `avgPosition` (
  `ymd` int(10) NOT NULL DEFAULT 20181213 COMMENT '年月日： yyyymmdd',
  `position` varchar(20) NOT NULL COMMENT '圈层名字',
  `bedroom_num` tinyint(4) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL COMMENT '平均单价',
  `total_price` decimal(10,2) NOT NULL COMMENT '平均总价',
  `build_area` decimal(10,2) NOT NULL COMMENT '平均建筑面积',
  `inside_area` decimal(10,2) NOT NULL COMMENT '平均套内面积',
  `num_house` smallint(6) NOT NULL COMMENT '在线房子套数',
  `follow` decimal(10,2) NOT NULL COMMENT '平均关注，热度',
  `take_look` decimal(10,2) NOT NULL COMMENT '平均带看，热度',
  PRIMARY KEY (`ymd`,`position`,`bedroom_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for house
-- ----------------------------
DROP TABLE IF EXISTS `house`;
CREATE TABLE `house` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `url` bigint(20) NOT NULL COMMENT '二手房地址',
  `housing_estate` varchar(20) NOT NULL COMMENT '小区',
  `position` varchar(20) NOT NULL COMMENT '位置',
  `square_metre` decimal(10,2) NOT NULL COMMENT '大小 平米',
  `unit_Price` float(11,0) NOT NULL COMMENT '单价元 基本都是整数',
  `total_price` float(11,0) NOT NULL COMMENT '总价万元 基本都是整数',
  `follow` int(11) NOT NULL COMMENT '关注量',
  `take_look` int(11) NOT NULL COMMENT '带看量',
  `pub_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '发布日期',
  PRIMARY KEY (`url`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38367 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for houseA
-- ----------------------------
DROP TABLE IF EXISTS `houseA`;
CREATE TABLE `houseA` (
  `id` bigint(20) NOT NULL COMMENT '二手房地址',
  `title` varchar(50) NOT NULL COMMENT '房屋标题',
  `housing_estate` varchar(20) NOT NULL COMMENT '小区',
  `position` varchar(20) NOT NULL COMMENT '位置',
  `district` varchar(20) NOT NULL COMMENT '行政区',
  `city` varchar(20) NOT NULL DEFAULT '成都' COMMENT '城市',
  `bedroom_num` tinyint(4) NOT NULL COMMENT '卧室数量',
  `livingroom_num` tinyint(4) NOT NULL COMMENT '客厅数量',
  `bathroom_num` tinyint(4) NOT NULL COMMENT '卫生间数量',
  `build_area` decimal(10,2) NOT NULL COMMENT '建筑面积',
  `inside_area` decimal(10,2) NOT NULL COMMENT '套内面积',
  `unit_price` decimal(10,2) NOT NULL COMMENT '单价元 基本都是整数',
  `total_price` decimal(10,2) NOT NULL COMMENT '总价万元 基本都是整数',
  `follow` int(11) NOT NULL COMMENT '关注量',
  `take_look` int(11) NOT NULL COMMENT '带看量',
  `pub_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '发布日期',
  `build_year` smallint(6) NOT NULL COMMENT '修建年代',
  `lastdeal_date` timestamp NULL DEFAULT NULL COMMENT '上一次交易时间',
  `yearlimit` varchar(20) NOT NULL COMMENT '年限，是否满两年或满五年',
  `use_type` varchar(20) NOT NULL COMMENT '普通住宅、公寓、别墅等等',
  `use_year` tinyint(4) NOT NULL COMMENT '使用年限，70/40',
  `ownership` varchar(20) NOT NULL COMMENT '商品房、小产权、单位分房等等',
  `fitment` varchar(20) NOT NULL COMMENT '装修情况',
  `elevator_num` tinyint(4) NOT NULL COMMENT '电梯数量',
  `house_num` tinyint(4) NOT NULL COMMENT '每层住户数',
  `structure` varchar(20) NOT NULL DEFAULT '' COMMENT '户型结构：平层、跃层',
  `build_structure` varchar(20) NOT NULL COMMENT '建筑结构，砖混',
  `floor` varchar(20) NOT NULL COMMENT '所在楼层',
  `tag` varchar(100) NOT NULL COMMENT '标签：自荐、优选等',
  `direction` varchar(20) NOT NULL COMMENT '朝向',
  `build_type` varchar(20) NOT NULL COMMENT '建筑类型',
  `updateTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '价格数据更新日期',
  `touchTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '检查数据时有数据时间，连续7天无数据，按下架处理',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for maininfo
-- ----------------------------
DROP TABLE IF EXISTS `maininfo`;
CREATE TABLE `maininfo` (
  `ymd` int(10) NOT NULL COMMENT '年月日',
  `num_house` int(10) NOT NULL,
  `avg_total_price` decimal(10,2) NOT NULL,
  `avg_unit_price` decimal(10,2) NOT NULL,
  `num_priceup` int(10) NOT NULL,
  `num_pricedown` int(10) NOT NULL,
  PRIMARY KEY (`ymd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pricelog
-- ----------------------------
DROP TABLE IF EXISTS `pricelog`;
CREATE TABLE `pricelog` (
  `id` bigint(20) NOT NULL COMMENT '链家编号',
  `unit_price` decimal(10,2) NOT NULL COMMENT '单价（元）',
  `total_price` decimal(10,2) NOT NULL COMMENT '总价（万元）',
  `unit_change` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '单价变化，降价为负数，涨价为正数',
  `total_change` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '总价变化，降价为负数，涨价为正数',
  `pricetrend` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '价格走势： up  /  down',
  `pricetype` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '价格类型：quote 报价, deal  成交',
  `thedate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '采集数据时间，价格变动时间',
  `createDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '数据创建时间',
  PRIMARY KEY (`id`,`total_price`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for room
-- ----------------------------
DROP TABLE IF EXISTS `room`;
CREATE TABLE `room` (
  `id` bigint(20) NOT NULL COMMENT '房屋ID',
  `title` varchar(20) NOT NULL COMMENT '名称，如卧室A',
  `area` decimal(10,2) NOT NULL COMMENT '面积，单位平方米',
  `direction` varchar(20) NOT NULL COMMENT '朝向',
  `window` varchar(20) NOT NULL COMMENT '窗户类型',
  PRIMARY KEY (`title`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
