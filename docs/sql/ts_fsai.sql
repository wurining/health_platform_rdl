/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50744
 Source Host           : localhost:3306
 Source Schema         : ts_fsai

 Target Server Type    : MySQL
 Target Server Version : 50744
 File Encoding         : 65001

 Date: 01/12/2025 22:38:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin_dept
-- ----------------------------
DROP TABLE IF EXISTS `admin_dept`;
CREATE TABLE `admin_dept`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '部门ID',
  `parent_id` int(11) NULL DEFAULT NULL COMMENT '父级编号',
  `dept_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '部门名称',
  `sort` int(11) NULL DEFAULT NULL COMMENT '排序',
  `leader` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系方式',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `status` int(11) NULL DEFAULT NULL COMMENT '状态(1开启,0关闭)',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '详细地址',
  `create_at` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_at` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_dept
-- ----------------------------
INSERT INTO `admin_dept` VALUES (1, 0, '仁济百草', 1, NULL, NULL, NULL, 1, '这是总公司', NULL, '2024-11-04 23:55:42', '2025-11-22 13:35:33');
INSERT INTO `admin_dept` VALUES (4, 1, '深圳分部', 2, 'None', '12312345679', '123qq.com', 1, '这是济南', NULL, '2024-11-04 23:55:42', '2025-11-22 13:35:46');
INSERT INTO `admin_dept` VALUES (5, 1, '广州分部', 4, 'None', '12312345679', 'None', 1, '这是唐山', NULL, '2024-11-04 23:55:42', '2025-11-22 13:35:56');
INSERT INTO `admin_dept` VALUES (7, 4, '罗湖店', 5, 'None', '12312345679', 'None', 1, '测试', NULL, '2024-11-04 23:55:42', '2025-11-22 13:35:52');
INSERT INTO `admin_dept` VALUES (8, 5, '越秀店', 5, 'None', 'None', 'None', 1, '测试部', NULL, '2024-11-04 23:55:42', '2025-11-22 13:36:01');

-- ----------------------------
-- Table structure for admin_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `admin_dict_data`;
CREATE TABLE `admin_dict_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典类型名称',
  `data_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典类型标识',
  `type_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典类型描述',
  `is_default` int(11) NULL DEFAULT NULL COMMENT '是否默认',
  `enable` int(11) NULL DEFAULT NULL COMMENT '是否开启',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_dict_data
-- ----------------------------

-- ----------------------------
-- Table structure for admin_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `admin_dict_type`;
CREATE TABLE `admin_dict_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典类型名称',
  `type_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典类型标识',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典类型描述',
  `enable` int(11) NULL DEFAULT NULL COMMENT '是否开启',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_dict_type
-- ----------------------------

-- ----------------------------
-- Table structure for admin_log
-- ----------------------------
DROP TABLE IF EXISTS `admin_log`;
CREATE TABLE `admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `uid` int(11) NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `success` int(11) NULL DEFAULT NULL,
  `user_agent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '浏览器类型',
  `os` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作系统',
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '地理位置',
  `create_time` datetime(0) NULL DEFAULT NULL,
  `operation_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作类型',
  `module_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '模块名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_log
-- ----------------------------
INSERT INTO `admin_log` VALUES (1, 'POST', 1, '/system/passport/login', 'admin', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'admin', 'Chrome', 'Windows 10/11', NULL, '2025-11-22 14:39:21', NULL, NULL);
INSERT INTO `admin_log` VALUES (2, 'POST', 1, '/passport/login', 'admin', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'admin', 'Chrome', 'Windows 10/11', NULL, '2025-11-22 23:10:15', NULL, NULL);
INSERT INTO `admin_log` VALUES (3, 'POST', NULL, '/system/passport/logout', '用户 admin 退出登录', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', NULL, 'Chrome', 'Windows 10/11', NULL, '2025-11-22 23:18:17', '新增', '登录认证');
INSERT INTO `admin_log` VALUES (4, 'POST', 1, '/passport/login', 'admin', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'admin', 'Chrome', 'Windows 10/11', NULL, '2025-11-22 23:18:26', NULL, NULL);
INSERT INTO `admin_log` VALUES (5, 'PUT', 1, '/system/user/editPassword', '用户管理-修改密码-成功', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'admin', 'Chrome', 'Windows 10/11', NULL, '2025-11-30 20:44:19', '修改密码', '用户管理');

-- ----------------------------
-- Table structure for admin_mail
-- ----------------------------
DROP TABLE IF EXISTS `admin_mail`;
CREATE TABLE `admin_mail`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '邮件编号',
  `receiver` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '收件人邮箱',
  `subject` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮件主题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '邮件正文',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '发送人id',
  `create_at` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_mail
-- ----------------------------

-- ----------------------------
-- Table structure for admin_photo
-- ----------------------------
DROP TABLE IF EXISTS `admin_photo`;
CREATE TABLE `admin_photo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `href` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `mime` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `size` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_photo
-- ----------------------------
INSERT INTO `admin_photo` VALUES (2, 'ScreenShot_2025-11-22_143233_082.png', '/_uploads/photos/ScreenShot_2025-11-22_143233_082.png', 'image/png', '376518', '2025-11-22 14:32:47');
INSERT INTO `admin_photo` VALUES (3, 'ScreenShot_2025-11-29_140541_274.png', '/_uploads/photos/ScreenShot_2025-11-29_140541_274.png', 'image/png', '40197', '2025-11-29 14:28:23');
INSERT INTO `admin_photo` VALUES (4, 'ScreenShot_2025-11-29_140541_274_1.png', '/_uploads/photos/ScreenShot_2025-11-29_140541_274_1.png', 'image/png', '40197', '2025-11-29 14:32:55');
INSERT INTO `admin_photo` VALUES (5, '11111.png', '/_uploads/photos/11111.png', 'image/png', '9574', '2025-11-29 17:17:53');
INSERT INTO `admin_photo` VALUES (6, '11111_1.png', '/_uploads/photos/11111_1.png', 'image/png', '9574', '2025-11-29 21:09:03');
INSERT INTO `admin_photo` VALUES (7, '11111_2.png', '/_uploads/photos/11111_2.png', 'image/png', '9574', '2025-11-29 21:10:49');
INSERT INTO `admin_photo` VALUES (8, '11111_3.png', '/_uploads/photos/11111_3.png', 'image/png', '9574', '2025-11-29 22:07:17');
INSERT INTO `admin_photo` VALUES (9, '81697541944F7DF9A08A47B29C3BAC2DF6C30666_size105_w1080_h1268.jpg', '/_uploads/photos/81697541944F7DF9A08A47B29C3BAC2DF6C30666_size105_w1080_h1268.jpg', 'image/jpeg', '113102', '2025-11-30 14:39:55');
INSERT INTO `admin_photo` VALUES (10, '142b-ef52a96211ac1c2412bd5032afa2c11f.jpg', '/_uploads/photos/142b-ef52a96211ac1c2412bd5032afa2c11f.jpg', 'image/jpeg', '164388', '2025-11-30 15:34:32');
INSERT INTO `admin_photo` VALUES (11, 'ec30-7539b79ed1bd4400d6c8f051940f3304.jpg', '/_uploads/photos/ec30-7539b79ed1bd4400d6c8f051940f3304.jpg', 'image/jpeg', '306101', '2025-11-30 17:22:20');
INSERT INTO `admin_photo` VALUES (12, '902f-bf72062e9ad46dfe080e2e98059fb951.png', '/_uploads/photos/902f-bf72062e9ad46dfe080e2e98059fb951.png', 'image/png', '647232', '2025-11-30 17:39:45');
INSERT INTO `admin_photo` VALUES (13, '142b-ef52a96211ac1c2412bd5032afa2c11f_1.jpg', '/_uploads/photos/142b-ef52a96211ac1c2412bd5032afa2c11f_1.jpg', 'image/jpeg', '164388', '2025-11-30 19:14:30');
INSERT INTO `admin_photo` VALUES (14, 'ec30-7539b79ed1bd4400d6c8f051940f3304_1.jpg', '/_uploads/photos/ec30-7539b79ed1bd4400d6c8f051940f3304_1.jpg', 'image/jpeg', '306101', '2025-11-30 20:38:00');
INSERT INTO `admin_photo` VALUES (15, '902f-bf72062e9ad46dfe080e2e98059fb951_1.png', '/_uploads/photos/902f-bf72062e9ad46dfe080e2e98059fb951_1.png', 'image/png', '647232', '2025-11-30 20:41:59');

-- ----------------------------
-- Table structure for admin_power
-- ----------------------------
DROP TABLE IF EXISTS `admin_power`;
CREATE TABLE `admin_power`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '权限编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限名称',
  `type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限类型',
  `code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限标识',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限路径',
  `open_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '打开方式',
  `parent_id` int(11) NULL DEFAULT NULL COMMENT '父类编号',
  `icon` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图标',
  `sort` int(11) NULL DEFAULT NULL COMMENT '排序',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  `enable` int(11) NULL DEFAULT NULL COMMENT '是否开启',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 84 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_power
-- ----------------------------
INSERT INTO `admin_power` VALUES (1, '组织管理', '0', NULL, NULL, NULL, 0, 'layui-icon layui-icon layui-icon layui-icon-group', 8, '2024-11-04 23:55:42', '2025-11-22 13:32:11', 1);
INSERT INTO `admin_power` VALUES (3, '用户管理', '1', 'system:user:main', '/system/user/', '_iframe', 1, 'layui-icon layui-icon-username', 1, '2024-11-04 23:55:42', '2025-11-07 00:01:48', 1);
INSERT INTO `admin_power` VALUES (4, '权限管理', '1', 'system:power:main', '/system/power/', '_iframe', 1, 'layui-icon layui-icon layui-icon-password', 4, '2024-11-04 23:55:42', '2025-11-22 14:16:26', 1);
INSERT INTO `admin_power` VALUES (9, '角色管理', '1', 'system:role:main', '/system/role', '_iframe', 1, 'layui-icon layui-icon-user', 2, '2024-11-04 23:55:42', '2025-11-07 00:02:09', 1);
INSERT INTO `admin_power` VALUES (12, '系统监控', '1', 'system:monitor:main', '/system/monitor', '_iframe', 60, 'layui-icon layui-icon layui-icon-vercode', 5, '2024-11-04 23:55:42', '2025-11-22 13:30:14', 1);
INSERT INTO `admin_power` VALUES (13, '日志管理', '1', 'system:log:main', '/system/log', '_iframe', 60, 'layui-icon layui-icon layui-icon-read', 4, '2024-11-04 23:55:42', '2025-11-22 13:30:26', 1);
INSERT INTO `admin_power` VALUES (17, '预约管理', '0', NULL, NULL, NULL, 0, 'layui-icon layui-icon layui-icon layui-icon-date', 1, '2024-11-04 23:55:42', '2025-11-16 21:46:08', 1);
INSERT INTO `admin_power` VALUES (18, '图片上传', '1', 'system:file:main', '/system/file', '_iframe', 60, 'layui-icon layui-icon layui-icon layui-icon-camera', 5, '2024-11-04 23:55:42', '2025-11-22 13:31:10', 1);
INSERT INTO `admin_power` VALUES (21, '权限增加', '2', 'system:power:add', '', '', 4, 'layui-icon layui-icon-add-circle', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (22, '用户增加', '2', 'system:user:add', '', '', 3, 'layui-icon layui-icon-add-circle', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (23, '用户编辑', '2', 'system:user:edit', '', '', 3, 'layui-icon layui-icon-rate', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (24, '用户删除', '2', 'system:user:remove', '', '', 3, '', 3, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (25, '权限编辑', '2', 'system:power:edit', '', '', 4, '', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (26, '用户删除', '2', 'system:power:remove', '', '', 4, '', 3, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (27, '用户增加', '2', 'system:role:add', '', '', 9, '', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (28, '角色编辑', '2', 'system:role:edit', '', '', 9, '', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (29, '角色删除', '2', 'system:role:remove', '', '', 9, '', 3, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (30, '角色授权', '2', 'system:role:power', '', '', 9, '', 4, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (31, '图片增加', '2', 'system:file:add', '', '', 18, '', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (32, '图片删除', '2', 'system:file:delete', '', '', 18, '', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (44, '数据字典', '1', 'system:dict:main', '/system/dict', '_iframe', 60, 'layui-icon layui-icon layui-icon-console', 6, '2024-11-04 23:55:42', '2025-11-22 13:30:39', 1);
INSERT INTO `admin_power` VALUES (45, '字典增加', '2', 'system:dict:add', '', '', 44, '', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (46, '字典修改', '2', 'system:dict:edit', '', '', 44, '', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (47, '字典删除', '2', 'system:dict:remove', '', '', 44, '', 3, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (48, '部门管理', '1', 'system:dept:main', '/system/dept', '_iframe', 1, 'layui-icon layui-icon-component', 3, '2024-11-04 23:55:42', '2025-11-22 13:28:34', 1);
INSERT INTO `admin_power` VALUES (49, '部门增加', '2', 'system:dept:add', '', '', 48, '', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (50, '部门编辑', '2', 'system:dept:edit', '', '', 48, '', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (51, '部门删除', '2', 'system:dept:remove', '', '', 48, '', 3, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (57, '邮件管理', '1', 'system:mail:main', '/system/mail', '_iframe', 60, 'layui-icon layui-icon ', 7, '2024-11-04 23:55:42', '2025-11-22 13:30:56', 1);
INSERT INTO `admin_power` VALUES (58, '邮件发送', '2', 'system:mail:add', '', '', 57, 'layui-icon layui-icon-ok-circle', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (59, '邮件删除', '2', 'system:mail:remove', '', '', 57, '', 2, '2024-11-04 23:55:42', '2024-11-04 23:55:42', 1);
INSERT INTO `admin_power` VALUES (60, '系统设置', '0', NULL, NULL, NULL, 0, 'layui-icon layui-icon-set-fill', 9, '2024-11-05 00:04:17', '2025-11-22 13:29:55', 1);
INSERT INTO `admin_power` VALUES (61, '门诊管理', '0', NULL, NULL, NULL, 0, 'layui-icon layui-icon layui-icon layui-icon layui-icon-cellphone-fine', 2, '2024-11-05 00:06:58', '2025-11-16 21:46:20', 1);
INSERT INTO `admin_power` VALUES (62, '门诊信息', '1', 'None', '/system/outpatients', '_iframe', 61, 'layui-icon layui-icon layui-icon layui-icon-template-1', 2, '2025-11-07 00:22:36', '2025-11-21 23:33:56', 1);
INSERT INTO `admin_power` VALUES (63, '患者管理', '0', NULL, NULL, NULL, 0, 'layui-icon layui-icon-username', 3, '2025-11-07 00:23:22', '2025-11-22 13:37:05', 1);
INSERT INTO `admin_power` VALUES (64, '患者总览', '1', 'None', '/system/patientsummary', '_iframe', 63, 'layui-icon layui-icon layui-icon layui-icon layui-icon layui-icon layui-icon layui-icon-chart', 2, '2025-11-07 00:24:16', '2025-11-22 23:14:14', 1);
INSERT INTO `admin_power` VALUES (66, '预约查询', '1', 'None', '/system/appointment/', '_iframe', 17, 'layui-icon layui-icon layui-icon layui-icon layui-icon-date', 1, '2025-11-12 23:30:04', '2025-11-13 00:26:13', 1);
INSERT INTO `admin_power` VALUES (67, '数据管理', '0', NULL, NULL, NULL, 0, 'layui-icon layui-icon-template-1', 4, '2025-11-16 21:47:33', '2025-11-16 21:47:33', 1);
INSERT INTO `admin_power` VALUES (68, '患者管理', '0', NULL, NULL, NULL, 67, 'layui-icon layui-icon layui-icon-username', 1, '2025-11-16 21:49:47', '2025-11-16 21:52:20', 1);
INSERT INTO `admin_power` VALUES (69, '自建数据库', '0', NULL, NULL, NULL, 67, 'layui-icon layui-icon layui-icon-align-left', 2, '2025-11-16 21:50:41', '2025-11-16 21:52:27', 1);
INSERT INTO `admin_power` VALUES (70, '统计报表', '0', NULL, NULL, NULL, 67, 'layui-icon layui-icon-chart-screen', 3, '2025-11-16 21:51:51', '2025-11-16 21:51:51', 1);
INSERT INTO `admin_power` VALUES (71, '患者信息', '1', 'None', '/system/patients', '_iframe', 68, 'layui-icon layui-icon layui-icon-username', 1, '2025-11-16 22:13:21', '2025-11-19 22:57:18', 1);
INSERT INTO `admin_power` VALUES (72, '患者病史', '1', 'None', '/system/patientmedicalhistories', '_iframe', 68, 'layui-icon layui-icon layui-icon layui-icon-headset', 2, '2025-11-16 22:14:25', '2025-11-19 23:34:48', 1);
INSERT INTO `admin_power` VALUES (73, '患者病程', '1', 'None', '/system/coursesofdisease', '_iframe', 68, 'layui-icon layui-icon layui-icon layui-icon-username', 3, '2025-11-16 22:15:25', '2025-11-21 22:00:01', 1);
INSERT INTO `admin_power` VALUES (74, '辅助检查', '1', 'None', '/system/examlib', '_iframe', 68, 'layui-icon layui-icon layui-icon layui-icon-refresh-3', 5, '2025-11-16 22:19:32', '2025-11-19 22:58:16', 1);
INSERT INTO `admin_power` VALUES (75, '病案归档', '1', 'None', '/system/records', '_iframe', 68, 'layui-icon layui-icon ', 7, '2025-11-16 22:21:37', '2025-11-19 22:48:41', 1);
INSERT INTO `admin_power` VALUES (76, '医学检查库', '1', NULL, '/', '_iframe', 69, 'layui-icon ', 1, '2025-11-16 22:22:13', '2025-11-16 22:22:13', 1);
INSERT INTO `admin_power` VALUES (77, '西药管理', '1', NULL, '/', '_iframe', 69, 'layui-icon ', 2, '2025-11-16 22:22:43', '2025-11-16 22:22:43', 1);
INSERT INTO `admin_power` VALUES (78, '诊断管理', '1', NULL, '/', '_iframe', 69, 'layui-icon ', 3, '2025-11-16 22:23:13', '2025-11-16 22:23:13', 1);
INSERT INTO `admin_power` VALUES (79, '预约管理', '1', NULL, '/', '_iframe', 69, 'layui-icon ', 5, '2025-11-16 22:23:42', '2025-11-16 22:23:42', 1);
INSERT INTO `admin_power` VALUES (80, '中药管理', '1', NULL, '/', '_iframe', 69, 'layui-icon ', 7, '2025-11-16 22:24:14', '2025-11-16 22:24:14', 1);
INSERT INTO `admin_power` VALUES (81, '综合统计', '1', NULL, '/', '_iframe', 70, 'layui-icon ', 1, '2025-11-16 22:24:55', '2025-11-16 22:24:55', 1);
INSERT INTO `admin_power` VALUES (82, '更新记录', '1', 'system:updatelog:main', '/system/updatelog', '_iframe', 60, 'layui-icon layui-icon-survey', 1, '2025-11-23 11:35:08', '2025-11-23 11:35:08', 1);
INSERT INTO `admin_power` VALUES (83, '诊断信息', '1', NULL, '/system/diagnostic', '_iframe', 68, 'layui-icon layui-icon-tabs', 2, '2025-11-29 14:41:45', '2025-11-29 14:41:45', 1);

-- ----------------------------
-- Table structure for admin_role
-- ----------------------------
DROP TABLE IF EXISTS `admin_role`;
CREATE TABLE `admin_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色名称',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '角色标识',
  `enable` int(11) NULL DEFAULT NULL COMMENT '是否启用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `details` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '详情',
  `sort` int(11) NULL DEFAULT NULL COMMENT '排序',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_role
-- ----------------------------
INSERT INTO `admin_role` VALUES (1, '管理员', 'admin', 1, NULL, '管理员', 1, '2024-11-04 23:55:42', '2024-11-04 23:55:42');
INSERT INTO `admin_role` VALUES (2, '普通管理员', 'common', 1, NULL, '只有查看，没有增删改权限', 2, '2024-11-04 23:55:42', '2025-11-22 14:25:04');

-- ----------------------------
-- Table structure for admin_role_power
-- ----------------------------
DROP TABLE IF EXISTS `admin_role_power`;
CREATE TABLE `admin_role_power`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `power_id` int(11) NULL DEFAULT NULL COMMENT '用户编号',
  `role_id` int(11) NULL DEFAULT NULL COMMENT '角色编号',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `power_id`(`power_id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  CONSTRAINT `admin_role_power_ibfk_1` FOREIGN KEY (`power_id`) REFERENCES `admin_power` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `admin_role_power_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_role_power
-- ----------------------------
INSERT INTO `admin_role_power` VALUES (1, 17, 2);
INSERT INTO `admin_role_power` VALUES (2, 3, 2);
INSERT INTO `admin_role_power` VALUES (3, 18, 2);
INSERT INTO `admin_role_power` VALUES (4, 4, 2);
INSERT INTO `admin_role_power` VALUES (5, 9, 2);
INSERT INTO `admin_role_power` VALUES (6, 48, 2);
INSERT INTO `admin_role_power` VALUES (7, 12, 2);
INSERT INTO `admin_role_power` VALUES (8, 44, 2);
INSERT INTO `admin_role_power` VALUES (9, 13, 2);
INSERT INTO `admin_role_power` VALUES (11, 61, 2);
INSERT INTO `admin_role_power` VALUES (12, 63, 2);

-- ----------------------------
-- Table structure for admin_updatelog
-- ----------------------------
DROP TABLE IF EXISTS `admin_updatelog`;
CREATE TABLE `admin_updatelog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '更新记录ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '更新标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '更新内容',
  `version` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '版本号',
  `update_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '更新类型',
  `create_id` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '创建人',
  `modify_id` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '修改人',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_create_time`(`create_time`) USING BTREE,
  INDEX `idx_version`(`version`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '更新日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_updatelog
-- ----------------------------
INSERT INTO `admin_updatelog` VALUES (1, '完善首页的数字显示', '1、首页更新', 'V0.4.1123', '功能更新', 1, 'admin', NULL, NULL, '2025-11-23 11:36:35', '2025-11-23 11:36:35');
INSERT INTO `admin_updatelog` VALUES (2, '患者总览功能预计完成70%左右；', '1、患者总览功能预计完成70%左右；\n2、患者管理的功能涉及的bug也修复了一部分。', 'V0.4.1129', '功能更新', 1, 'admin', 1, 'admin', '2025-11-29 23:55:28', '2025-11-29 23:55:41');

-- ----------------------------
-- Table structure for admin_user
-- ----------------------------
DROP TABLE IF EXISTS `admin_user`;
CREATE TABLE `admin_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `realname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '真实名字',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '头像',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '哈希密码',
  `enable` int(11) NULL DEFAULT NULL COMMENT '启用',
  `dept_id` int(11) NULL DEFAULT NULL COMMENT '部门id',
  `create_at` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_at` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_user
-- ----------------------------
INSERT INTO `admin_user` VALUES (1, 'admin', '超级管理员', '/static/system/admin/images/avatar.jpg', '要是不能把握时机，就要终身蹭蹬，一事无成！', 'pbkdf2:sha256:600000$HbSUAxHhfjAMH9SP$d570d669ff66afe561241e7c3334f40f82ed87265b75ed2c693c581c872e9890', 1, 1, '2024-11-04 23:55:42', '2025-11-30 20:44:19');
INSERT INTO `admin_user` VALUES (2, 'drzhang', '张主任', '/static/system/admin/images/avatar.jpg', '要是不能把握时机，就要终身蹭蹬，一事无成！', 'pbkdf2:sha256:150000$cRS8bYNh$adb57e64d929863cf159f924f74d0634f1fecc46dba749f1bfaca03da6d2e3ac', 1, 1, '2024-11-04 23:55:42', '2025-11-22 13:59:25');
INSERT INTO `admin_user` VALUES (3, 'drliu', '刘教授', '/static/system/admin/images/avatar.jpg', '要是不能把握时机，就要终身蹭蹬，一事无成！', 'pbkdf2:sha256:150000$skME1obT$6a2c20cd29f89d7d2f21d9e373a7e3445f70ebce3ef1c3a555e42a7d17170b37', 1, 4, '2024-11-04 23:55:42', '2025-11-22 13:59:59');

-- ----------------------------
-- Table structure for admin_user_role
-- ----------------------------
DROP TABLE IF EXISTS `admin_user_role`;
CREATE TABLE `admin_user_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户编号',
  `role_id` int(11) NULL DEFAULT NULL COMMENT '角色编号',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `admin_user_role_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `admin_user_role_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `admin_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin_user_role
-- ----------------------------
INSERT INTO `admin_user_role` VALUES (1, 1, 1);
INSERT INTO `admin_user_role` VALUES (2, 2, 2);
INSERT INTO `admin_user_role` VALUES (3, 3, 2);

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('96eb87438fa5');

-- ----------------------------
-- Table structure for renji_appointment
-- ----------------------------
DROP TABLE IF EXISTS `renji_appointment`;
CREATE TABLE `renji_appointment`  (
  `AppointmentID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '预约ID',
  `PatientID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '患者ID',
  `AppointmentTime` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '预约时间',
  `Remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`AppointmentID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_appointment
-- ----------------------------
INSERT INTO `renji_appointment` VALUES ('1641f619-6bb3-4218-ab64-3c7b50972e85', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '2025-10-19 00:00:00', '点点滴滴', 1, '超级管理员', '2025-10-19 12:10:26', 1, '超级管理', '2025-11-22 00:09:31');
INSERT INTO `renji_appointment` VALUES ('48ee5cca-3ac4-41e0-8977-1518def4fcad', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '2025-10-20 00:00:00', '放放风', 1, '超级管理员', '2025-10-20 12:18:17', 1, '超级管理', '2025-11-22 00:09:22');
INSERT INTO `renji_appointment` VALUES ('523d2f47-6628-407b-b799-c229fa87aceb', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '2025-10-17 00:00:00', '点点滴滴', 1, '超级管理员', '2025-10-17 12:20:26', 1, '超级管理', '2025-11-22 00:18:26');
INSERT INTO `renji_appointment` VALUES ('89844bf0-68cb-4e6b-b6bb-27c721796af1', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', '2025-11-22 04:57:00', '对对对', 1, '超级管理', '2025-11-22 00:58:08', 1, '超级管理', '2025-11-22 00:58:08');
INSERT INTO `renji_appointment` VALUES ('8ce7eb48-4b43-4ade-9ea8-f6e6aad00781', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '2025-11-26 22:00', '测试预约', 1, '超级管理员', '2025-11-26 20:53:33', 1, '超级管理员', '2025-11-26 20:53:33');
INSERT INTO `renji_appointment` VALUES ('8ea6841f-15c2-423d-93dc-2197dc83ab42', '2628f8fd-7c94-47c4-8845-65d1d2680a11', '2025-10-19 00:00:00', NULL, 1, '超级管理员', '2025-10-18 14:35:33', NULL, NULL, NULL);
INSERT INTO `renji_appointment` VALUES ('9ed40e4e-0273-40f4-8ea4-9c13b1694a36', 'a67bfd41-a097-4e20-83de-f19008f7715d', '2025-10-06 00:00:00', NULL, 1, '超级管理员', '2025-10-06 15:21:59', NULL, NULL, NULL);
INSERT INTO `renji_appointment` VALUES ('9f3dd4c2-8adf-45e4-aec5-44d20b6d47a0', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', '2025-11-22 18:09:00', '加号', 1, '超级管理', '2025-11-22 13:09:33', 1, '超级管理员', '2025-11-22 14:43:58');
INSERT INTO `renji_appointment` VALUES ('a9134906-4653-4432-9a67-98f4085675c6', 'a67bfd41-a097-4e20-83de-f19008f7715d', '2025-10-14 00:00:00', NULL, 1, '超级管理员', '2025-10-14 10:32:14', NULL, NULL, NULL);
INSERT INTO `renji_appointment` VALUES ('d82db495-a72b-4bc1-be48-bbe355eb753a', '2628f8fd-7c94-47c4-8845-65d1d2680a11', '2025-10-18 00:00:00', NULL, 1, '超级管理员', '2025-10-18 14:35:25', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for renji_auxiliaryexaminationes
-- ----------------------------
DROP TABLE IF EXISTS `renji_auxiliaryexaminationes`;
CREATE TABLE `renji_auxiliaryexaminationes`  (
  `ExaminationID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '检查ID',
  `RecordID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '病历ID',
  `ExaminationType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '检查类型',
  `ExaminerID` int(11) NULL DEFAULT NULL COMMENT '检查归属',
  `ExameTime` datetime(0) NULL DEFAULT NULL COMMENT '检查时间',
  `Diagnosis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '辅助检查内容',
  `AttachMents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件',
  `Remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`ExaminationID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_auxiliaryexaminationes
-- ----------------------------
INSERT INTO `renji_auxiliaryexaminationes` VALUES ('d758162b-3e8a-4194-b436-4ca124a6e8d2', '2628f8fd-7c94-47c4-8845-65d1d2680a11', '43b2294e-45ee-4599-89a9-055250be4c7d', NULL, NULL, 'X', 'Upload/Tables/renji_AuxiliaryExaminationes/202510191833371156/屏幕截图 2025-02-04 113912.png', NULL, 1, '超级管理员', '2025-10-19 18:33:38', NULL, NULL, NULL);
INSERT INTO `renji_auxiliaryexaminationes` VALUES ('ef39fdf0-7c7a-429e-a9b4-c77b810ee9bb', '2628f8fd-7c94-47c4-8845-65d1d2680a11', '43b2294e-45ee-4599-89a9-055250be4c7d', NULL, '2025-10-14 00:00:00', 'XXZZ', NULL, NULL, 1, '超级管理员', '2025-10-14 11:05:17', 1, '超级管理员', '2025-10-19 23:19:59');

-- ----------------------------
-- Table structure for renji_cnmedicine
-- ----------------------------
DROP TABLE IF EXISTS `renji_cnmedicine`;
CREATE TABLE `renji_cnmedicine`  (
  `MedicineID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '检查ID',
  `MedicineName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中药名称',
  `MedicineType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '中药类型',
  `MedicineInstruction` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '药品说明',
  `MedicineUse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '用法用量',
  `Remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`MedicineID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_cnmedicine
-- ----------------------------
INSERT INTO `renji_cnmedicine` VALUES ('c408ca0e-779a-47b7-ac16-dde6da16ffda', '百合', '成品', NULL, NULL, NULL, 1, '超级管理员', '2025-10-06 14:26:56', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for renji_coursesofdisease
-- ----------------------------
DROP TABLE IF EXISTS `renji_coursesofdisease`;
CREATE TABLE `renji_coursesofdisease`  (
  `CourseID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '病程ID',
  `PatientID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '患者ID',
  `UserID` int(11) NULL DEFAULT NULL COMMENT '医师',
  `CourseType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '病程类型',
  `CourseTime` datetime(0) NULL DEFAULT NULL COMMENT '病程时间',
  `CurrentDisease` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '现病史',
  `TreatmentPlan` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '治疗方案',
  `AttachMents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件',
  `Remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`CourseID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_coursesofdisease
-- ----------------------------
INSERT INTO `renji_coursesofdisease` VALUES ('0e673f9f-dd81-4c3e-81ab-4fdfd54ce536', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', 1, '复查', '2025-11-30 00:00:00', '佛挡杀佛水电费是的', '<p>fsdfsdfsdfds&nbsp;</p>\n<p>fdsfsdfsd&nbsp; &nbsp;fdsfsdfds&nbsp;</p>\n<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">\n<tbody>\n<tr>\n<td style=\"width: 31.3715%;\">fdsfsddfsdfs</td>\n<td style=\"width: 31.3715%;\">dfsfdsfdfds</td>\n<td style=\"width: 31.3758%;\">dsffdsfsdf</td>\n</tr>\n<tr>\n<td style=\"width: 31.3715%;\">fdsffsdfds</td>\n<td style=\"width: 31.3715%;\">sdffdsfsdfds</td>\n<td style=\"width: 31.3758%;\">sdfsdfsd</td>\n</tr>\n</tbody>\n</table>', '[\"/_uploads/photos/ec30-7539b79ed1bd4400d6c8f051940f3304.jpg\", \"/_uploads/photos/902f-bf72062e9ad46dfe080e2e98059fb951.png\"]', NULL, 1, '超级管理员', '2025-11-30 17:22:23', 1, '超级管理员', '2025-11-30 17:44:34');
INSERT INTO `renji_coursesofdisease` VALUES ('2fcfbef5-6098-48fa-9220-8630310d3f99', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', 1, 'Second', '2025-10-22 00:00:00', '佛挡杀佛水电费都是', '<p>发多少分多少粉丝77777</p>\n<p>发的书法大赛</p>', NULL, NULL, 1, '超级管理员', '2025-10-20 12:43:37', 1, '超级管理员', '2025-11-30 20:37:19');
INSERT INTO `renji_coursesofdisease` VALUES ('5b472804-2bde-46f5-9f64-7a0d19449b23', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', 1, 'First', '2025-10-20 00:00:00', 'asaddddddfdfsf', 'sfsdsdsdfsdffsdf dfsfsdfsddf ', '[\"/_uploads/photos/81697541944F7DF9A08A47B29C3BAC2DF6C30666_size105_w1080_h1268.jpg\"]', NULL, 1, '超级管理员', '2025-10-20 12:41:34', 1, '超级管理员', '2025-11-30 14:39:58');
INSERT INTO `renji_coursesofdisease` VALUES ('9edd3fb6-d717-42c7-8035-46411d99973d', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', 1, '复查', '2025-11-30 00:00:00', '发的所发生的', '<p>fdsfsdsdfs fsdfsfds</p>\n<p>dsfsdfsdfsdfsdfsd fsdfdsfsd</p>\n<p>dfsfsdfdsfsdfsdfd df&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;fdsfsdfdsfsd&nbsp;</p>', '[\"/_uploads/photos/142b-ef52a96211ac1c2412bd5032afa2c11f.jpg\"]', '发的所发生的33333', 1, '超级管理员', '2025-11-30 15:34:34', 1, '超级管理员', '2025-11-30 17:35:12');
INSERT INTO `renji_coursesofdisease` VALUES ('c49b5543-32fc-4d80-9dff-2b2e51e476ea', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', 1, '初诊', '2025-11-29 00:00:00', '但是对方都是 \n\n点点滴滴\n分手的方式地方都是', '<p>fsfdsfsdfdlfdslf d的时间浪费的时间77777</p>\n<p>佛挡杀佛就是的&nbsp; &nbsp;发多少分多少分多少</p>\n<table style=\"border-collapse: collapse; width: 100%;\" border=\"1\">\n<tbody>\n<tr>\n<td style=\"width: 31.3715%;\">发的所发生的</td>\n<td style=\"width: 31.3715%;\">发的书法大赛</td>\n<td style=\"width: 31.3758%;\">发的所发生的</td>\n</tr>\n<tr>\n<td style=\"width: 31.3715%;\">发的书法大赛</td>\n<td style=\"width: 31.3715%;\">对方是否第三方</td>\n<td style=\"width: 31.3758%;\">发的顺丰的所发生的</td>\n</tr>\n</tbody>\n</table>', NULL, '发多少分多少收到', 1, '超级管理员', '2025-11-29 16:14:29', 1, '超级管理员', '2025-11-30 20:37:04');

-- ----------------------------
-- Table structure for renji_diagnostic
-- ----------------------------
DROP TABLE IF EXISTS `renji_diagnostic`;
CREATE TABLE `renji_diagnostic`  (
  `DiagnosticID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '诊断ID',
  `PatientID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '患者ID',
  `Diagnosis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '诊断（多标签，JSON数组格式）',
  `OtherHospitalDiagnosis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '其他医院诊断',
  `Pathology` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '病理',
  `AttachMents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件（多图片，JSON数组格式）',
  `Remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`DiagnosticID`) USING BTREE,
  INDEX `idx_patient_id`(`PatientID`) USING BTREE,
  CONSTRAINT `fk_diagnostic_patient` FOREIGN KEY (`PatientID`) REFERENCES `renji_patients` (`PatientID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '诊断信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_diagnostic
-- ----------------------------
INSERT INTO `renji_diagnostic` VALUES ('8b32e5f4-4b1f-492a-b139-cc7074e94aef', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '[\"AAA\"]', NULL, '对对对', '[\"/_uploads/photos/11111_2.png\"]', '佛挡杀佛未查询', 1, 'admin', NULL, NULL, '2025-11-29 21:11:00', '2025-11-29 21:11:00');
INSERT INTO `renji_diagnostic` VALUES ('9bd7fc10-be3f-4c56-92d6-094f333842f0', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', '[\"AAA\"]', NULL, '对对对', '[\"/_uploads/photos/11111_2.png\"]', '佛挡杀佛未查询哈哈哈', 1, 'admin', 1, 'admin', '2025-11-29 21:11:39', '2025-11-29 21:14:22');
INSERT INTO `renji_diagnostic` VALUES ('eb6116ed-4890-442c-9078-2af9868f7af7', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '[\"懒病\", \"心病\", \"好奇\"]', '有的', '不好意思说 ', '[\"/_uploads/photos/ScreenShot_2025-11-29_140541_274_1.png\", \"/_uploads/photos/11111.png\"]', '找医生去点点滴滴85964965486', 1, 'admin', 1, 'admin', '2025-11-29 14:06:00', '2025-11-29 17:18:00');

-- ----------------------------
-- Table structure for renji_examlib
-- ----------------------------
DROP TABLE IF EXISTS `renji_examlib`;
CREATE TABLE `renji_examlib`  (
  `ExamID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '检查ID',
  `ExamName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '检查名称',
  `PatientID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '患者ID',
  `Remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `AttachMents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`ExamID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '检查' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_examlib
-- ----------------------------
INSERT INTO `renji_examlib` VALUES ('38a04efa-8cc7-4bfa-8008-91291f6abbb3', '眼科检查', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '测试表', '[\"/_uploads/photos/902f-bf72062e9ad46dfe080e2e98059fb951_1.png\"]', 1, '超级管理员', '2025-11-30 20:42:03', 1, 'admin', '2025-11-30 20:42:03');
INSERT INTO `renji_examlib` VALUES ('7065aac0-fa9d-4b6d-9b97-0a0be9bea59e', '胸部CT检查', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '大大方方的佛挡杀佛当时的方式第三方\n发多少分多少分多少------=-=-=-=++++\n++++++', '[\"/_uploads/photos/11111_3.png\", \"/_uploads/photos/142b-ef52a96211ac1c2412bd5032afa2c11f_1.jpg\"]', 1, '超级管理员', '2025-11-29 22:07:19', 1, 'admin', '2025-11-30 19:14:40');
INSERT INTO `renji_examlib` VALUES ('77c158cf-fa12-4129-a339-ed48d0eb1bbe', 'CT', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', '再确定一下', NULL, 1, '超级管理员', '2025-11-29 21:53:58', 1, 'admin', '2025-11-29 21:53:58');
INSERT INTO `renji_examlib` VALUES ('bf4b6f29-ffc9-4551-b03b-7ad79c5d90ee', '外科检查', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '现场检查，没发现问题', '[\"/_uploads/photos/ec30-7539b79ed1bd4400d6c8f051940f3304_1.jpg\"]', 1, '超级管理员', '2025-11-30 20:38:01', 1, 'admin', '2025-11-30 20:38:01');

-- ----------------------------
-- Table structure for renji_patientmedicalhistories
-- ----------------------------
DROP TABLE IF EXISTS `renji_patientmedicalhistories`;
CREATE TABLE `renji_patientmedicalhistories`  (
  `HistoryID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '病史ID',
  `PatientID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '患者ID',
  `PastHistory` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '既往史',
  `PersonalHistory` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '个人史',
  `MarriageHistory` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '婚育史',
  `FamilyHistory` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '家族史',
  `AllergyHistory` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '过敏史',
  `MenstrualHistory` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '月经史',
  `Other` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '其它',
  `Summary` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '小结',
  `CustomerType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '推荐人',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`HistoryID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '患者病史' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_patientmedicalhistories
-- ----------------------------
INSERT INTO `renji_patientmedicalhistories` VALUES ('1f6e5f0b-6228-4b10-a416-8dd9ff849e85', 'cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', '发的书法大赛', '发多少的方式', '发的书法大赛', '分手的方式的', '佛挡杀佛第三方', '一个接一个', '很过分很过分', '官方很过分', NULL, 1, '超级管理员', '2025-11-29 21:32:28', 1, '超级管理员', '2025-11-29 21:32:28');
INSERT INTO `renji_patientmedicalhistories` VALUES ('5dba19e6-9ff6-448f-8d18-7d4fb3dab13a', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '辅导费地方', '大幅度发', '发的房东的', '放的地方', '疯疯癫癫', 'None', '放对方的地方', '对对对放放风柔柔弱弱v', '点点滴滴', 1, '超级管理员', '2025-10-20 12:44:37', 1, '超级管理员', '2025-11-29 17:16:43');
INSERT INTO `renji_patientmedicalhistories` VALUES ('6f279ad4-46ab-4ac0-bf08-7d4be744a9b6', 'a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '分手的方式的', '退热贴', '他人儿', '他人儿', '贴退热贴', '退热贴', '退热贴', '贴退热贴', NULL, 1, '超级管理员', '2025-11-29 21:34:22', 1, '超级管理员', '2025-11-29 21:34:22');

-- ----------------------------
-- Table structure for renji_patients
-- ----------------------------
DROP TABLE IF EXISTS `renji_patients`;
CREATE TABLE `renji_patients`  (
  `PatientID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '患者ID',
  `Name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '患者姓名',
  `PatientNo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '患者编号',
  `Sex` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别',
  `Nation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '民族',
  `Birthday` date NULL DEFAULT NULL COMMENT '生日',
  `ContactPhone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话',
  `Address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系地址',
  `IdNumber` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '证件号',
  `Career` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '职业',
  `Remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注信息',
  `CustomerType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '推荐人',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`PatientID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_patients
-- ----------------------------
INSERT INTO `renji_patients` VALUES ('a3d6bfde-ab1d-4669-85aa-b3b8f97e6c26', '小罗同学', '202511112', '男', '汉族', '1977-11-11', '13489093456', '深圳市龙岗区花花街道', '4332992810210128218', '码工', '开始干活了吧 1111', '罗峰', 1, '超级管理员', '2025-11-11 23:06:09', 1, '超级管理员', '2025-11-29 23:00:18');
INSERT INTO `renji_patients` VALUES ('cc9b3ea7-ed91-48e3-b36e-9865e9c6111e', '小王同学', '20251023009', '女', '汉族', '2015-06-10', '13489899090', '北京市房山区天津路130号', '442551201506107823', '张诗雅', '首次接诊滚滚滚对对对', '小张', 1, '超级管理员', '2025-10-23 15:29:55', 1, '超级管理员', '2025-11-30 12:53:45');

-- ----------------------------
-- Table structure for renji_records
-- ----------------------------
DROP TABLE IF EXISTS `renji_records`;
CREATE TABLE `renji_records`  (
  `RecordID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '基本病情Id',
  `RecordNumber` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '病案编号',
  `PatientID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '患者ID',
  `RecordTime` datetime(0) NULL DEFAULT NULL COMMENT '初诊时间',
  `Diagnosis` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '诊断',
  `OtherDiagnosis` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '他院诊断',
  `Pathology` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '病理',
  `AttachMents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '附件',
  `Remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`RecordID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_records
-- ----------------------------
INSERT INTO `renji_records` VALUES ('4f85e80a-d2a0-459b-8aea-ffdbd0acde9a', NULL, 'a67bfd41-a097-4e20-83de-f19008f7715d', '2025-10-06 00:00:00', '552d88be-99ee-4d6f-9232-8ab172ac9b24', 'EXTRA', 'CT', NULL, NULL, 1, '超级管理员', '2025-10-06 15:09:52', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for renji_westmedicine
-- ----------------------------
DROP TABLE IF EXISTS `renji_westmedicine`;
CREATE TABLE `renji_westmedicine`  (
  `MedicineID` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '西药ID',
  `MedicineName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '西药名称',
  `MedicineType` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '西药类型',
  `MedicineInstruction` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '药品说明',
  `MedicineUse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '用法用量',
  `Remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '备注',
  `CreateID` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `Creator` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `CreateDate` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `ModifyID` int(11) NULL DEFAULT NULL COMMENT '修改人ID',
  `Modifier` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '修改人',
  `ModifyDate` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`MedicineID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of renji_westmedicine
-- ----------------------------
INSERT INTO `renji_westmedicine` VALUES ('b4aae269-efdb-4651-8f78-a0c98c4ae008', '青霉素', '抗生素', NULL, NULL, NULL, 1, '超级管理员', '2025-10-06 14:27:52', NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
