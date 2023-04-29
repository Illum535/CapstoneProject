import sqlite3

class Collection:
    """
    Attributes:
    self.tblname - Name of the table 
    self.collname - Name of the collection

    Methods:
    add_record(self, record) - Checks whether CCA/activity is present in the collection before adding the record into the table
    
    view_record(self, name) - Returns the student's class in the collection with the corresponding name, if present

    view_all(self) - Returns all records in the specified table
    
    edit_record(self, name, record) - Replaces the record with corresponding name with new record, if present
    """
    def __init__(self, dbname, tblname):
        self._dbname = dbname
        self._tblname = tblname

    

    def add_record(self, record):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        params = tuple(record.values())
        name = params[0]
        check = self.view_record(name)
        
        if check == 'RECORD DOESNT EXIST GRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA':
            id = self.add_id()
            params = list(params)
            params.insert(0, id)
            params = tuple(params)
            if self._tblname == 'CCA':
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """

            else:
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?, ?, ?);        
                """
        
            c.execute(QUERY, params)

        else:
            return 'RECORD ALREADY EXISTS GRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        conn.commit()
        conn.close()

    def add_id(self):
        data = self.view_all()
        num = len(data)
        return num + 1


    def view_record(self, name):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "Name"=?;
        """
        val = (name,)
        c.execute(VIEW, val)
        result = c.fetchone()
        if result == None:
            return 'RECORD DOESNT EXIST GRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        conn.commit()
        conn.close()
        result = list(result)
        result.pop(0)
        result = tuple(result)
        return result

    
    def view_all(self):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        VIEW = f"""
            SELECT * FROM {self._tblname};
        """
        c.execute(VIEW)
        result = c.fetchall()
        for i, x in enumerate(result):
            x = list(x)
            x.pop(0)
            x = tuple(x)
            result[i] = x
            
        return result


    

    def edit_record(self, name, record):
        details = list(record.values())
        keys = list(record.keys())
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        
        check = self.view_record(name)
        
        if check == 'RECORD DOESNT EXIST GRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA':
            return check
        data = self.view_all()
        id = data.index(check) + 1
        print(keys)
        if self._tblname == 'CCA':
            query = f"""UPDATE {self._tblname} 
                        SET "id" = ?,
                            {keys[0]} = ?,
                            {keys[1]} = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], name)
        else:
            query = f"""UPDATE {self._tblname}
                        SET "id" = ?,
                            {keys[0]} = ?,
                            {keys[1]} = ?,
                            {keys[2]} = ?,
                            {keys[3]} = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], details[2], details[3], name)
        c.execute(query, val)
        conn.commit()
        conn.close()


class ActivityCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'Activity')


class CCACollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'CCA')

class ClassCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'Class')

class StudentCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'Student')

class SubjectCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'Subjects')
