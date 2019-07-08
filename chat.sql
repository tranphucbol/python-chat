CREATE TABLE accounts (
    user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    status SMALLINT(1) NOT NULL,
    UNIQUE (username, email)
);

CREATE TABLE friends (
    user_id BIGINT NOT NULL,
    friend_id BIGINT NOT NULL,
    status SMALLINT(1) NOT NULL,
    PRIMARY KEY (user_id,friend_id),
    FOREIGN KEY (user_id) REFERENCES accounts(user_id),
    FOREIGN KEY (friend_id) REFERENCES accounts(user_id)
);

CREATE TABLE channels (
    channel_id BIGINT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE messages (
    channel_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    message_id BIGINT NOT NULL PRIMARY KEY,
    content TEXT NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (author_id) REFERENCES accounts(user_id)
);
