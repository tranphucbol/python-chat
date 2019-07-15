CREATE TABLE users (
    user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    status SMALLINT(1) NOT NULL,
    UNIQUE (username, email)
);

CREATE TABLE friends (
    user_id BIGINT NOT NULL,
    friend_id BIGINT NOT NULL,
    status SMALLINT(1) NOT NULL,
    PRIMARY KEY (user_id,friend_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (friend_id) REFERENCES users(user_id)
);

CREATE TABLE channels (
    channel_id BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE messages (
    channel_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    message_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

CREATE TABLE users_channels (
    channel_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    seen DATETIME NOT NULL,
    PRIMARY KEY (channel_id, user_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE sessions (
    user_id BIGINT NOT NULL PRIMARY,
    session_id VARCHAR(50) NOT NULL
)