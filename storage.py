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

            elif self._tblname == 'Activity':
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?, ?, ?);        
                """

            elif self._tblname == 'Class':
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """

            elif self._tblname == 'Student':
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?, ?, ?);        
                """
                
            elif self._tblname == 'Subjects':
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """

            
            elif self._tblname == 'student_class':
                student = 'Student'
                VIEW = f"""
                    SELECT * FROM {student} 
                    WHERE "Name"=?;
                """
                val = (name, )
                c.execute(VIEW, val)
                student_data = c.fetchone()
                student_id = student_data[0]

                theclass = 'Class'
                VIEW = f"""
                    SELECT * FROM {theclass} 
                    WHERE "Name"=?;
                """
                val = (params[-1], )
                c.execute(VIEW, val)
                class_data = c.fetchone()
                class_id = class_data[0]

                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?);        
                """

                params = (student_id, class_id)
                
                
                
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

        if self._tblname == 'student_class':
            
            student = 'Student'
            VIEW = f"""
            SELECT * FROM {student} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return 'RECORD DOESNT EXIST GRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "student_id"=?;
            """
            val = (student_data[0], )
            c.execute(VIEW, val)
            studentclass_data = c.fetchone()
            
            theclass = 'Class'
            VIEW = f"""
            SELECT * FROM {theclass} 
            WHERE "id"=?;
            """
            val = (studentclass_data[1], )
            c.execute(VIEW, val)
            class_data = c.fetchone()

            conn.commit()
            conn.close()
            return (student_data[1], class_data[1])
            
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
        print(result)

        if self._tblname == 'student_class':
            
            data = []
            for x in result:
                
                student = 'Student'
                VIEW = f"""
                SELECT * FROM {student} 
                WHERE "id"=?;
                """
                val = (x[0], )
                c.execute(VIEW, val)
                student_data = c.fetchone()
    
                theclass = 'Class'
                VIEW = f"""
                SELECT * FROM {theclass} 
                WHERE "id"=?;
                """
                val = (x[1], )
                c.execute(VIEW, val)
                class_data = c.fetchone()

                data.append((student_data[1], class_data[1]))

            conn.close()
            return data
                
            
        for i, x in enumerate(result):
            x = list(x)
            x.pop(0)
            x = tuple(x)
            result[i] = x

        conn.close()
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
        if self._tblname == 'CCA':
            query = f"""UPDATE {self._tblname} 
                        SET "id" = ?,
                            "Name" = ?,
                            "Type" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], name)

        elif self._tblname == 'Class':
            query = f"""UPDATE {self._tblname} 
                        SET "id" = ?,
                            "Name" = ?,
                            "Level" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], name)
            
        elif self._tblname == 'Activity':
            query = f"""UPDATE {self._tblname}
                        SET "id" = ?,
                            "Name" = ?,
                            "Description" = ?,
                            "Start_Date" = ?,
                            "End_Date" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], details[2], details[3], name)

        elif self._tblname == 'Student':
            query = f"""UPDATE {self._tblname}
                        SET "id" = ?,
                            "Name" = ?,
                            "Age" = ?,
                            "Year_Enrolled" = ?,
                            "Graduating_Year" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], details[2], details[3], name)

        elif self._tblname == 'Subjects':
            query = f"""UPDATE {self._tblname} 
                        SET "id" = ?,
                            "Name" = ?,
                            "Level" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, details[0], details[1], name)


        elif self._tblname == 'student_class':
            
            student = 'Student'
            VIEW = f"""SELECT * FROM {student} 
                        WHERE "Name" = ?;"""
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()

            theclass = 'Class'
            VIEW = f"""SELECT * FROM {theclass} 
                        WHERE "Name" = ?;"""
            val = (details[-1], )
            c.execute(VIEW, val)
            class_data = c.fetchone()
            
            query = f"""UPDATE {self._tblname} 
                        SET "student_id" = ?,
                            "class_id" = ?
                        WHERE "student_id" = ?
                        ;"""
            val = (student_data[0], class_data[0], student_data[0])
            
        c.execute(query, val)
        conn.commit()
        conn.close()



    

    def delete_record(self, name):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        check = self.view_record(name)
        
        if check == 'RECORD DOESNT EXIST GRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA':
            return check

        if self._tblname == 'student_class':
            
            student = 'Student'
            VIEW = f"""SELECT * FROM {student} 
                        WHERE "Name"=?;"""
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()

            query = f"""
                DELETE FROM {self._tblname}
                WHERE "student_id" = ?;
            """
            val = (student_data[0], )
            c.execute(query, val)
            conn.commit()
            conn.close()
            return ''

        query = f"""
            DELETE FROM {self._tblname}
            WHERE "Name" = ?;
        """
        val = (name, )
        c.execute(query, val)
        conn.commit()
        conn.close()
        self.reorder()


    

    def reorder(self):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        VIEW = f"""
            SELECT * FROM {self._tblname};
        """
        c.execute(VIEW)
        result = c.fetchall()
        for i, x in enumerate(result):
            if x[0] != (i+1):
                temp = {}
                for y in x:
                    if x.index(y) != 0:
                        temp[y] = y
                print(temp)
                self.edit_record(x[1], temp)
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

class StudentClassCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'student_class')
