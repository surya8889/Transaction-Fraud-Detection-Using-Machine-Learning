import sqlite3 as sql


class Database:
    
     def init(self, filename):
        self.filename = filename

        self.conn = sql.connect(filename)
        self.cursor = self.__conn.cursor()
        self.create_database()

    def create_database(self):
        """
        Creates the Table if it does not exist
        """
        
        sqlstr= "CREATE TABLE IF NOT EXISTS card_master(id INTEGER PRIMARY KEY AUTOINCREMENT,cardno TEXT,expiredate TEXT, pin TEXT, balance FLOAT,status INTEGER)"

        try:
            self.cursor.execute(sqlstr)
            self.conn.commit()
        except:
            pass
    
    def get_all_entries(self):
        print("db in")
        """
        Returns all of entries in the database
        """
        self.__cursor.execute("SELECT * FROM card_master")
        return self.__cursor.fetchall()

    def get_by_id(self, idtofind):
        """
        Returns a entry by the given id
        """
        logging.debug(f"getting data by id: {idtofind}")
        self.__cursor.execute(f"SELECT name,expiredate,desc,cat FROM card_master WHERE id='{idtofind}'")
        return self.__cursor.fetchone()

    def add_entry(self,name, expiredate, pin, bal,status):
        """
        Adds a new entry to the database
        """
        self.cursor.execute(
            "INSERT INTO main(cardno,expiredate,pin,balance,status) VALUES(?,?,?,?,?)", (name, expiredate, pin, bal,status))
        self.conn.commit()
        
     def close(self):
        """
        Closes the database
        """
        self.conn.close()
