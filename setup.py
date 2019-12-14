import db

#Create a table
db.cursor().execute("CREATE TABLE `users` (`id` INT NOT NULL, `name` TEXT NOT NULL, `age` INT NOT NULL, `sex` TEXT NOT NULL, latitude FLOAT, longitude FLOAT, PRIMARY KEY(`id`))")
