CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS incomes(
   user_id INTEGER NOT NULL,
   title TEXT NOT NULL,       
   income TEXT NOT NULL,
   FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS expenses(
   user_id INTEGER NOT NULL,
   title TEXT NOT NULL,       
   expense TEXT NOT NULL,
   created_at DATETIME NOT NULL DEFAULT current_timestamp,
   FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS goals(
   user_id INTEGER NOT NULL,
   title TEXT NOT NULL,
   money_count TEXT NOT NULL,
   savings TEXT NOT NULL DEFAULT '0',
   FOREIGN KEY (user_id) REFERENCES users (id)
)