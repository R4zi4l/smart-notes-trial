SELECT @@GLOBAL.max_allowed_packet INTO @max_allowed_packet;
SET GLOBAL group_concat_max_len = @max_allowed_packet;

DROP DATABASE IF EXISTS `smartnotes`;
CREATE DATABASE `smartnotes` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `smartnotes`;

SOURCE ./database/setup.sql
