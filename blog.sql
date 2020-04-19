BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS `User` (
	`userid`	INTEGER,
	`username`	TEXT,
	`password`	TEXT,
	`is_admin`	TEXT,
	`is_logged_in`	INTEGER,
	PRIMARY KEY(`userid`)
);

CREATE TABLE IF NOT EXISTS `Article` (
	`articleid`	INTEGER,
	`title`	TEXT,
	`message`	TEXT,
	`keywords`	TEXT,
    `date`	TEXT,
	PRIMARY KEY(`articleid`),
	FOREIGN KEY(userid) REFERENCES Article(articleid) ON DELETE SET NULL
	FOREIGN KEY(userid) REFERENCES Article(articleid) ON UPDATE CASCADE
);



CREATE TABLE IF NOT EXISTS `Comment` (
	`commentid` INTEGER,
	`author`	TEXT,
	`message`	TEXT,
	`date`	TEXT,
	PRIMARY KEY(`commentid`),
	FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE CASCADE
	FOREIGN KEY (userid) REFERENCES User(userid) ON UPDATE CASCADE
);

COMMIT;