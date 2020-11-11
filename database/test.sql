SELECT @@GLOBAL.max_allowed_packet INTO @max_allowed_packet;
SET GLOBAL group_concat_max_len = @max_allowed_packet;

DROP DATABASE IF EXISTS `smartnotestest`;
CREATE DATABASE `smartnotestest` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `smartnotestest`;

SOURCE ./database/setup.sql

SET @user_id = 'b2f0683c-cc42-11ea-93df-0a0027000007';
INSERT INTO `user` (`id`, `updated`, `email`, `username`, `password`) VALUE(@user_id, NOW(), 'first email', 'first username', 'first password');


-- SET @event_1_id = 'a3196364-cdb8-11ea-a8dd-0a0027000007';
-- INSERT INTO `event` (`id`, `owner`, `updated`, `text`) VALUE(@event_1_id, @user_id, NOW(), 'first event');


SET @note_1_id = 'b0540414-cc4f-11ea-93df-0a0027000007';
INSERT INTO `note` (`id`, `owner`, `updated`, `title`, `text`) VALUE(@note_1_id, @user_id, NOW(), 'first note', 'first note text');

SET @note_2_id = '2f1322c5-cc55-11ea-93df-0a0027000007';
INSERT INTO `note` (`id`, `owner`, `updated`, `title`, `text`) VALUE(@note_2_id, @user_id, NOW(), 'second note', 'second note text');


-- SET @board_1_id = 'e3b9ce33-cc50-11ea-93df-0a0027000007';
-- INSERT INTO `board` (`id`, `owner`, `updated`, `title`, `text`) VALUE(@board_1_id, @user_id, NOW(), 'first', 'FIRST BOARD');

-- SET @board_2_id = '0d61630a-cc51-11ea-93df-0a0027000007';
-- INSERT INTO `board` (`id`, `owner`, `updated`, `title`, `text`) VALUE(@board_2_id, @user_id, NOW(), 'second', 'SECOND BOARD');


-- INSERT INTO `boardnote` (`owner`, `board`, `note`, `updated`) VALUE(@user_id, @board_1_id, @note_1_id, NOW());
-- INSERT INTO `boardnote` (`owner`, `board`, `note`, `updated`) VALUE(@user_id, @board_2_id, @note_1_id, NOW());
-- INSERT INTO `boardnote` (`owner`, `board`, `note`, `updated`) VALUE(@user_id, @board_1_id, @note_2_id, NOW());
