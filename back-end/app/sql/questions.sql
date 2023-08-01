DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS answer;

CREATE TABLE question(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    analysis TEXT NOT NULL,
    type TEXT NOT NULL,
    level TEXT NOT NULL
);

CREATE TABLE answer(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    corrent INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES question (id)
);