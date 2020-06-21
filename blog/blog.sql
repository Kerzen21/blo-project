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

--usersnames = [ 1, 2,,3 ,3 3, ]

--votes_aritcle1 = upvote:[1, 2, 3, 4] + downvote:[5, 4, 56, 67]
-- votes_article1 [vote1(upvote:1, downvote:0), vote2(upvote:0, downvote:1), ... ]


-- 12 | 0 | 1 | 0 | 4

CREATE TABLE IF NOT EXISTS `Votes` (
	`articleid` INTEGER,
	`commentid` INTEGER,
	`upvote` INTEGER,
	`downvote` INTEGER,
	`userid` INTEGER,
	FOREIGN KEY (userid) REFERENCES User(userid) ON DELETE SET NULL
	FOREIGN KEY (userid) REFERENCES User(userid) ON UPDATE CASCADE
	FOREIGN KEY (articleid) REFERENCES Articles(articleid) ON DELETE CASCADE
	FOREIGN KEY (articleid) REFERENCES Articles(articleid) ON UPDATE CASCADE
	FOREIGN KEY (commentid) REFERENCES Comments(commentid) ON DELETE CASCADE
	FOREIGN KEY (commentid) REFERENCES Comments(commentid) ON UPDATE CASCADE
);	

COMMIT;