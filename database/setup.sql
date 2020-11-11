CREATE TABLE `owner` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `table` VARCHAR(255) CHARACTER SET ascii NOT NULL,

  PRIMARY KEY(`id`)
);


CREATE TABLE `session` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii DEFAULT NULL,
  `updated` DATETIME(3) NOT NULL,
  
  `started` DATETIME NOT NULL,
  `expired` DATETIME NOT NULL,
  
  PRIMARY KEY(`id`),
  FOREIGN KEY(`owner`) REFERENCES `owner`(`id`) ON DELETE CASCADE
);


CREATE TABLE `settings` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `device` VARCHAR(4096) NOT NULL,
  `updated` DATETIME(3) NOT NULL,
  `settings` TEXT,

  PRIMARY KEY(`id`),
  FOREIGN KEY(`owner`) REFERENCES `owner`(`id`) ON DELETE CASCADE
);


CREATE TABLE `user` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,
  
  `email` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,

  PRIMARY KEY(`id`),
  FOREIGN KEY(`id`) REFERENCES `owner`(`id`) ON DELETE CASCADE
);

CREATE TABLE `user_history` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,
  `action` VARCHAR(255) NOT NULL,

  `email` VARCHAR(255) DEFAULT NULL,
  `username` VARCHAR(255) DEFAULT NULL,
  `password` VARCHAR(255) DEFAULT NULL,

  PRIMARY KEY(`id`, `updated`),
  FOREIGN KEY(`id`) REFERENCES `owner`(`id`) ON DELETE CASCADE
);


CREATE TABLE `entity` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `table` VARCHAR(255) CHARACTER SET ascii NOT NULL,

  PRIMARY KEY(`id`, `owner`),
  FOREIGN KEY(`owner`) REFERENCES `owner`(`id`) ON DELETE CASCADE
);


-- CREATE TABLE `event` (
--   `id` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `updated` DATETIME(3) NOT NULL,

--   `text` TEXT DEFAULT NULL,
--   `scheduled` DATETIME DEFAULT NULL,
--   `done` DATETIME DEFAULT NULL,
--   `income` FLOAT NOT NULL DEFAULT 0,
--   `expense` FLOAT NOT NULL DEFAULT 0,
--   `source` CHAR(36) CHARACTER SET ascii DEFAULT NULL,

--   PRIMARY KEY(`id`, `owner`),
--   FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE,
--   FOREIGN KEY(`source`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
-- );

-- CREATE TABLE `event_history` (
--   `id` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `updated` DATETIME(3) NOT NULL,
--   `action` VARCHAR(255) NOT NULL,

--   `text` TEXT DEFAULT NULL,
--   `scheduled` DATETIME DEFAULT NULL,
--   `done` DATETIME DEFAULT NULL,
--   `income` FLOAT DEFAULT NULL,
--   `expense` FLOAT DEFAULT NULL,
--   `source` CHAR(36) CHARACTER SET ascii DEFAULT NULL,

--   PRIMARY KEY(`id`, `owner`, `updated`),
--   FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
-- );


CREATE TABLE `note` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,

  `title` VARCHAR(255) DEFAULT NULL,
  `text` TEXT DEFAULT NULL,

  PRIMARY KEY(`id`, `owner`),
  FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
);

CREATE TABLE `note_history` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,
  `action` VARCHAR(255) NOT NULL,

  `title` VARCHAR(255) DEFAULT NULL,
  `text` TEXT DEFAULT NULL,

  PRIMARY KEY(`id`, `owner`, `updated`),
  FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
);


-- CREATE TABLE `board` (
--   `id` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `updated` DATETIME(3) NOT NULL,

--   `title` VARCHAR(255) DEFAULT NULL,
--   `text` TEXT DEFAULT NULL,

--   PRIMARY KEY(`id`, `owner`),
--   FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
-- );

-- CREATE TABLE `board_history` (
--   `id` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `updated` DATETIME(3) NOT NULL,
--   `action` VARCHAR(255) NOT NULL,

--   `title` VARCHAR(255) DEFAULT NULL,
--   `text` TEXT DEFAULT NULL,

--   PRIMARY KEY(`id`, `owner`, `updated`),
--   FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
-- );


CREATE TABLE `category` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,

  `title` VARCHAR(255) DEFAULT NULL,
  `text` TEXT DEFAULT NULL,
  `parent` CHAR(36) CHARACTER SET ascii DEFAULT NULL,

  PRIMARY KEY(`id`, `owner`),
  FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE,
  FOREIGN KEY(`parent`, `owner`) REFERENCES `category`(`id`, `owner`) ON DELETE CASCADE
);

CREATE TABLE `category_history` (
  `id` CHAR(36) CHARACTER SET ascii NOT NULL,
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,
  `action` VARCHAR(255) NOT NULL,

  `title` VARCHAR(255) DEFAULT NULL,
  `text` TEXT DEFAULT NULL,
  `parent` CHAR(36) CHARACTER SET ascii DEFAULT NULL,

  PRIMARY KEY(`id`, `owner`, `updated`),
  FOREIGN KEY(`id`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
);


-- CREATE TABLE `boardnote` (
--   `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `board` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `note` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `updated` DATETIME(3) NOT NULL,

--   PRIMARY KEY(`owner`, `board`, `note`),
--   FOREIGN KEY(`board`, `owner`) REFERENCES `board`(`id`, `owner`) ON DELETE CASCADE,
--   FOREIGN KEY(`note`, `owner`) REFERENCES `note`(`id`, `owner`) ON DELETE CASCADE
-- );

-- CREATE TABLE `boardnote_history` (
--   `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `board` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `note` CHAR(36) CHARACTER SET ascii NOT NULL,
--   `updated` DATETIME(3) NOT NULL,
--   `action` VARCHAR(255) NOT NULL,

--   PRIMARY KEY(`owner`, `board`, `note`, `updated`),
--   FOREIGN KEY(`board`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE,
--   FOREIGN KEY(`note`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
-- );


CREATE TABLE `categoryentity` (
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `category` CHAR(36) CHARACTER SET ascii NOT NULL,
  `entity` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,

  PRIMARY KEY(`owner`, `category`, `entity`),
  FOREIGN KEY(`category`, `owner`) REFERENCES `category`(`id`, `owner`) ON DELETE CASCADE,
  FOREIGN KEY(`entity`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
);

CREATE TABLE `categoryentity_history` (
  `owner` CHAR(36) CHARACTER SET ascii NOT NULL,
  `category` CHAR(36) CHARACTER SET ascii NOT NULL,
  `entity` CHAR(36) CHARACTER SET ascii NOT NULL,
  `updated` DATETIME(3) NOT NULL,
  `action` VARCHAR(255) NOT NULL,

  PRIMARY KEY(`owner`, `category`, `entity`, `updated`),
  FOREIGN KEY(`category`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE,
  FOREIGN KEY(`entity`, `owner`) REFERENCES `entity`(`id`, `owner`) ON DELETE CASCADE
);


CREATE TRIGGER `insert_user` BEFORE INSERT ON `user`
FOR EACH ROW
  INSERT IGNORE INTO `owner` (`id`, `table`) VALUE(NEW.id, 'user');

-- CREATE TRIGGER `insert_event` BEFORE INSERT ON `event`
-- FOR EACH ROW
--   INSERT IGNORE INTO `entity` (`id`, `owner`, `table`) VALUE(NEW.id, NEW.owner, 'event');

CREATE TRIGGER `insert_note` BEFORE INSERT ON `note`
FOR EACH ROW
  INSERT IGNORE INTO `entity` (`id`, `owner`, `table`) VALUE(NEW.id, NEW.owner, 'note');

-- CREATE TRIGGER `insert_board` BEFORE INSERT ON `board`
-- FOR EACH ROW
--   INSERT IGNORE INTO `entity` (`id`, `owner`, `table`) VALUE(NEW.id, NEW.owner, 'board');

CREATE TRIGGER `insert_category` BEFORE INSERT ON `category`
FOR EACH ROW
  INSERT IGNORE INTO `entity` (`id`, `owner`, `table`) VALUE(NEW.id, NEW.owner, 'category');


CREATE TRIGGER `insert_user_history` AFTER INSERT ON `user`
FOR EACH ROW
  INSERT INTO `user_history` (`action`, `id`, `updated`, `email`, `username`, `password`)
    VALUE('insert', NEW.id, NEW.updated, NEW.email, NEW.username, NEW.password);

CREATE TRIGGER `update_user_history` AFTER UPDATE ON `user`
FOR EACH ROW
  INSERT INTO `user_history` (`action`, `id`, `updated`, `email`, `username`, `password`)
    VALUE('update', NEW.id, NEW.updated, NEW.email, NEW.username, NEW.password);

CREATE TRIGGER `delete_user_history` AFTER DELETE ON `user`
FOR EACH ROW
  INSERT INTO `user_history` (`action`, `id`, `updated`, `email`, `username`, `password`)
    VALUE('delete', OLD.id, NOW(), OLD.email, OLD.username, OLD.password);


-- CREATE TRIGGER `insert_event_history` AFTER INSERT ON `event`
-- FOR EACH ROW
--   INSERT INTO `event_history` (`action`, `id`, `owner`, `updated`, `text`, `scheduled`, `done`, `income`, `expense`, `source`)
--     VALUE('insert', NEW.id, NEW.owner, NEW.updated, NEW.text, NEW.scheduled, NEW.done, NEW.income, NEW.expense, NEW.source);

-- CREATE TRIGGER `update_event_history` AFTER UPDATE ON `event`
-- FOR EACH ROW
--   INSERT INTO `event_history` (`action`, `id`, `owner`, `updated`, `text`, `scheduled`, `done`, `income`, `expense`, `source`)
--     VALUE('update', NEW.id, NEW.owner, NEW.updated, NEW.text, NEW.scheduled, NEW.done, NEW.income, NEW.expense, NEW.source);

-- CREATE TRIGGER `delete_event_history` AFTER DELETE ON `event`
-- FOR EACH ROW
--   INSERT INTO `event_history` (`action`, `id`, `owner`, `updated`, `text`, `scheduled`, `done`, `income`, `expense`, `source`)
--     VALUE('delete', OLD.id, OLD.owner, NOW(), OLD.text, OLD.scheduled, OLD.done, OLD.income, OLD.expense, OLD.source);


CREATE TRIGGER `insert_note_history` AFTER INSERT ON `note`
FOR EACH ROW
  INSERT INTO `note_history` (`action`, `id`, `owner`, `updated`, `text`, `title`)
    VALUE('insert', NEW.id, NEW.owner, NEW.updated, NEW.text, NEW.title);

CREATE TRIGGER `update_note_history` AFTER UPDATE ON `note`
FOR EACH ROW
  INSERT INTO `note_history` (`action`, `id`, `owner`, `updated`, `text`, `title`)
    VALUE('update', NEW.id, NEW.owner, NEW.updated, NEW.text, NEW.title);

CREATE TRIGGER `delete_note_history` AFTER DELETE ON `note`
FOR EACH ROW
  INSERT INTO `note_history` (`action`, `id`, `owner`, `updated`, `text`, `title`)
    VALUE('delete', OLD.id, OLD.owner, NOW(), OLD.text, OLD.title);


-- CREATE TRIGGER `insert_board_history` AFTER INSERT ON `board`
-- FOR EACH ROW
--   INSERT INTO `board_history` (`action`, `id`, `owner`, `updated`, `title`, `text`)
--     VALUE('insert', NEW.id, NEW.owner, NEW.updated, NEW.title, NEW.text);

-- CREATE TRIGGER `update_board_history` AFTER UPDATE ON `board`
-- FOR EACH ROW
--   INSERT INTO `board_history` (`action`, `id`, `owner`, `updated`, `title`, `text`)
--     VALUE('update', NEW.id, NEW.owner, NEW.updated, NEW.title, NEW.text);

-- CREATE TRIGGER `delete_board_history` AFTER DELETE ON `board`
-- FOR EACH ROW
--   INSERT INTO `board_history` (`action`, `id`, `owner`, `updated`, `title`, `text`)
--     VALUE('delete', OLD.id, OLD.owner, NOW(), OLD.title, OLD.text);


CREATE TRIGGER `insert_category_history` AFTER INSERT ON `category`
FOR EACH ROW
  INSERT INTO `category_history` (`action`, `id`, `owner`, `updated`, `title`, `text`, `parent`)
    VALUE('insert', NEW.id, NEW.owner, NEW.updated, NEW.title, NEW.text, NEW.parent);

CREATE TRIGGER `update_category_history` AFTER UPDATE ON `category`
FOR EACH ROW
  INSERT INTO `category_history` (`action`, `id`, `owner`, `updated`, `title`, `text`, `parent`)
    VALUE('update', NEW.id, NEW.owner, NEW.updated, NEW.title, NEW.text, NEW.parent);

CREATE TRIGGER `delete_category_history` AFTER DELETE ON `category`
FOR EACH ROW
  INSERT INTO `category_history` (`action`, `id`, `owner`, `updated`, `title`, `text`, `parent`)
    VALUE('delete', OLD.id, OLD.owner, NOW(), OLD.title, OLD.text, OLD.parent);


-- CREATE TRIGGER `insert_boardnote_history` AFTER INSERT ON `boardnote`
-- FOR EACH ROW
--   INSERT INTO `boardnote_history` (`action`, `owner`, `board`, `note`, `updated`)
--     VALUE('insert', NEW.owner, NEW.board, NEW.note, NEW.updated);

-- CREATE TRIGGER `update_boardnote_history` AFTER UPDATE ON `boardnote`
-- FOR EACH ROW
--   INSERT INTO `boardnote_history` (`action`, `owner`, `board`, `note`, `updated`)
--     VALUE('update', NEW.owner, NEW.board, NEW.note, NEW.updated);

-- CREATE TRIGGER `delete_boardnote_history` AFTER DELETE ON `boardnote`
-- FOR EACH ROW
--   INSERT INTO `boardnote_history` (`action`, `owner`, `board`, `note`, `updated`)
--     VALUE('delete', OLD.owner, OLD.board, OLD.note, NOW());


CREATE TRIGGER `insert_categoryentity_history` AFTER INSERT ON `categoryentity`
FOR EACH ROW
  INSERT INTO `categoryentity_history` (`action`, `owner`, `category`, `entity`, `updated`)
    VALUE('insert', NEW.owner, NEW.category, NEW.entity, NEW.updated);

CREATE TRIGGER `update_categoryentity_history` AFTER UPDATE ON `categoryentity`
FOR EACH ROW
  INSERT INTO `categoryentity_history` (`action`, `owner`, `category`, `entity`, `updated`)
    VALUE('update', NEW.owner, NEW.category, NEW.entity, NEW.updated);

CREATE TRIGGER `delete_categoryentity_history` AFTER DELETE ON `categoryentity`
FOR EACH ROW
  INSERT INTO `categoryentity_history` (`action`, `owner`, `category`, `entity`, `updated`)
    VALUE('delete', OLD.owner, OLD.category, OLD.entity, NOW());
