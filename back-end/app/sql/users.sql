DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_permission;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account VARCHAR(64) NOT NULL,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    permission_id INTEGER NOT NULL DEFAULT 0
)


CREATE TABLE role(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_id INTEGER NOT NULL,
    permission_name VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    create_time TEXT NOT NULL,
    FOREIGN KEY (permission_id) REFERENCES user(permission_id)
)