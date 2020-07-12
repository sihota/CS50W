-- books table ---
DROP TABLE IF EXISTS books;

CREATE TABLE books(
   id SERIAL NOT NULL PRIMARY KEY,
   isbn VARCHAR(10) NOT NULL,
   title VARCHAR NOT NULL,
   author VARCHAR NOT NULL,
   year INTEGER NOT NULL
);

CREATE INDEX isbn_index ON books (isbn);
-- books table ---

-- books review table ---
DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews(
  id SERIAL NOT NULL PRIMARY KEY,
  rating INTEGER NOT NULL,
  review TEXT,
  book_id INTEGER NOT NULL REFERENCES books,
  user_id INTEGER NOT NULL REFERENCES users
);
CREATE INDEX book_index ON reviews(book_id);
CREATE INDEX user_index ON reviews(user_id);
-- books review table ---

-- user table ---
--https://www.meetspaceapp.com/2016/04/12/passwords-postgresql-pgcrypto.html
CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users;

--id SERIAL NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
CREATE TABLE users(
  id SERIAL NOT NULL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password TEXT NOT NULL
);

CREATE INDEX username_index ON users(username);
-- user table ---
