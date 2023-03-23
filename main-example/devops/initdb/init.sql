CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4(),
    email TEXT,
    username VARCHAR(128),
    display_name VARCHAR(128),
    password TEXT,
    active BOOLEAN DEFAULT true,
    legal timestamp DEFAULT NOW(),
    created timestamp DEFAULT NOW(),
    PRIMARY KEY(id),
    UNIQUE(email),
    UNIQUE(username)
);
CREATE INDEX user_email ON users(email);
CREATE INDEX user_display_name ON users(display_name);

CREATE TABLE tokens (
    id uuid DEFAULT uuid_generate_v4(),
    userid uuid
    expiry timestamp DEFAULT (NOW() + interval '2 weeks')
    CONSTRAINT post_userid_fk
        FOREIGN KEY (userid)
            REFERENCES users(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
)

CREATE TABLE posts (
    id uuid DEFAULT uuid_generate_v4(),
    title VARCHAR(128),
    content TEXT,
    userid uuid,
    visible BOOLEAN DEFAULT true,
    created timestamp DEFAULT NOW(),
    PRIMARY KEY(id),
    CONSTRAINT post_userid_fk
        FOREIGN KEY (userid)
            REFERENCES users(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX post_userid ON posts(userid);

CREATE TABLE comments (
    id uuid DEFAULT uuid_generate_v4(),
    userid uuid,
    postid uuid,
    content TEXT,
    visible BOOLEAN DEFAULT true,
    created timestamp DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT comment_userid_fk
        FOREIGN KEY (userid)
            REFERENCES users(id)
            ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT comment_postid_fk
        FOREIGN KEY (postid)
            REFERENCES posts(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX comment_post ON comments(postid);

CREATE TABLE likes (
    id uuid DEFAULT uuid_generate_v4(),
    userid uuid,
    postid uuid,
    created timestamp DEFAULT NOW(),
    active BOOLEAN DEFAULT true,
    PRIMARY KEY (id),
    CONSTRAINT like_userid_fk
        FOREIGN KEY (userid)
            REFERENCES users(id)
            ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT like_postid_fk
        FOREIGN KEY (postid)
            REFERENCES posts(id)
            ON UPDATE CASCADE ON DELETE RESTRICT
);
CREATE INDEX like_postid ON likes(postid);
CREATE INDEX like_userid ON likes(userid);