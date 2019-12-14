import db

class User ():
    def __init__(self, id, age):
        self.id = id
        self.age = age

    def create(self):
        querytoerrors = "SELECT COUNT(*) FROM `demoniac` WHERE id = %s"
        if db.cursor().execute(querytoerrors, self.id) == 0:
            querytocreate = "INSERT INTO `demoniac` (id, age) VALUES (%s, %s);"
            db.cursor().execute(querytocreate, (self.id, self.age))  
        else:
            print("Are you trying to create an existing user, don't you prefer an update?")
    
    def update(self):
        querytoupdate = "UPDATE `demoniac` SET age = %s WHERE id = %s;"
        db.cursor().execute(querytoupdate, (self.age, self.id))