BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS `Users` (
	`userid`	INTEGER,
	`username`	TEXT,
	`password`	TEXT,
	`is_admin`	INTEGER,
	`is_logged_in`	INTEGER,
	PRIMARY KEY(`userid`)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_username ON Users (username);

CREATE TABLE IF NOT EXISTS `Articles` (
	`articleid`	INTEGER,
	`userid` INTEGER,
	`title`	TEXT,
	`message`	TEXT,
	`keywords`	TEXT,
    `date`	TEXT,
	PRIMARY KEY(`articleid`),
	FOREIGN KEY(`userid`) REFERENCES User(`userid`)  ON DELETE SET NULL
	FOREIGN KEY(`userid`) REFERENCES User(`userid`)  ON UPDATE CASCADE
);
-- Article
-- articleid : 12
-- userid : 4


CREATE TABLE IF NOT EXISTS `Comments` (
	`commentid` INTEGER,
	`articleid` INTEGER,
	`userid` INTEGER,
	`author`	TEXT,
	`message`	TEXT,
	`date`	TEXT,
	PRIMARY KEY(`commentid`),
	FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE SET NULL
	FOREIGN KEY (userid) REFERENCES User(userid) ON UPDATE CASCADE
	FOREIGN KEY (articleid) REFERENCES Articles(articleid) ON DELETE CASCADE
	FOREIGN KEY (articleid) REFERENCES Articles(articleid) ON UPDATE CASCADE
);
COMMIT;