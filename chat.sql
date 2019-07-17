CREATE TABLE users (
    user_id CHAR(36) NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    status SMALLINT(1) NOT NULL,
    UNIQUE (username)
);

CREATE TABLE friends (
    user_id CHAR(36) NOT NULL,
    friend_id CHAR(36) NOT NULL,
    status SMALLINT(1) NOT NULL,
    PRIMARY KEY (user_id,friend_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (friend_id) REFERENCES users(user_id)
);

CREATE TABLE channels (
    channel_id CHAR(36) NOT NULL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE messages (
    channel_id CHAR(36) NOT NULL,
    author_id CHAR(36) NOT NULL,
    message_id CHAR(36) NOT NULL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

CREATE TABLE users_channels (
    channel_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    seen DATETIME NOT NULL,
    PRIMARY KEY (channel_id, user_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE sessions (
    user_id CHAR(36) NOT NULL,
    session_id CHAR(32) NOT NULL,
    PRIMARY KEY(user_id, session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);