DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS answer;

CREATE TABLE question(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    analysis TEXT NOT NULL,
    type TEXT NOT NULL,
    level TEXT NOT NULL,
    point REAL NOT NULL
);

CREATE TABLE answer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    correct INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES question (id)
);

DROP TABLE IF EXISTS testpaper;
DROP TABLE IF EXISTS testpaper_question;

CREATE TABLE testpaper(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration TEXT NOT NULL,
    name TEXT NOT NULL,
    passline REAL NOT NULL
);

CREATE TABLE testpaper_question(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    testpaper_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES question(id),
    FOREIGN KEY (testpaper_id) REFERENCES testpaper(id)
);