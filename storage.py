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
        
            
        if self._tblname == 'CCA':
            check = self.view_record(record)
            if check == None:
                id = self.add_id()
                params = list(params)
                params.insert(0, id)
                params = tuple(params)
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """
            else:
                return False

        elif self._tblname == 'Activity':
            check = self.view_record(record)
            if check == None:
                id = self.add_id()
                params = list(params)
                params.insert(0, id)
                params = tuple(params)
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?, ?, ?);        
                """
            else:
                return False

        elif self._tblname == 'Class':
            check = self.view_record(record)
            if check == None:
                id = self.add_id()
                params = list(params)
                params.insert(0, id)
                params = tuple(params)
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """
            else:
                return False

        elif self._tblname == 'Student':
            check = self.view_record(record)
            if check == None:
                id = self.add_id()
                params = list(params)
                params.insert(0, id)
                params = tuple(params)
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?, ?, ?);        
                """
            else:
                return False
            
            
        elif self._tblname == 'Subjects':
            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "Name"=? AND "Level"=?;
            """ 
            val = (params[0], params[1])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                id = self.add_id()
                params = list(params)
                params.insert(0, id)
                params = tuple(params)
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """
            else:
                return False

        
        elif self._tblname == 'student_class':
            student = 'Student'
            VIEW = f"""
            SELECT * FROM {student} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False

            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "student_id"=?;
            """
            val = (student_data[0], )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                id = self.add_id()
                params = list(params)
                params.insert(0, id)
                params = tuple(params)
            
                student_id = student_data[0]
    
                theclass = 'Class'
                VIEW = f"""
                    SELECT * FROM {theclass} 
                    WHERE "Name"=?;
                """
                val = (params[-1], )
                c.execute(VIEW, val)
                class_data = c.fetchone()
                if class_data == None:
                    return False
                class_id = class_data[0]
    
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?);        
                """
    
                params = (student_id, class_id)

            else:
                return False


        elif self._tblname == 'cca_activity':
            cca = 'CCA'
            VIEW = f"""
                SELECT * FROM {cca} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            cca_data = c.fetchone()
            if cca_data == None:
                return False
            cca_id = cca_data[0]

            act = 'Activity'
            VIEW = f"""
                SELECT * FROM {act} 
                WHERE "Name"=?;
            """
            val = (params[-1], )
            c.execute(VIEW, val)
            act_data = c.fetchone()
            if act_data == None:
                return False
            act_id = act_data[0]


            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "cca_id"=? AND "activity_id"=?;
            """
            val = (cca_id, act_id)
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?);        
                """
    
                params = (cca_id, act_id)
            else:
                return False
                
        elif self._tblname == 'student_subject':
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False
            student_id = student_data[0]

            sub = 'Subjects'
            VIEW = f"""
                SELECT * FROM {sub} 
                WHERE "Name"=? AND "Level"=?;
            """
            val = (params[1], params[-1])
            c.execute(VIEW, val)
            sub_data = c.fetchone()
            if sub_data == None:
                return False
            sub_id = sub_data[0]

            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "student_id"=? AND "subject_id"=?;
            """
            val = (student_id, sub_id)
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?);        
                """
    
                params = (student_id, sub_id)
            else:
                return False



        elif self._tblname == 'student_activity':
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False
            student_id = student_data[0]

            act = 'Activity'
            VIEW = f"""
                SELECT * FROM {act} 
                WHERE "Name"=?;
            """
            val = (params[1], )
            c.execute(VIEW, val)
            act_data = c.fetchone()
            if act_data == None:
                return False
            act_id = act_data[0]


            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "student_id"=? AND "activity_id"=?;
            """
            val = (student_id, act_id)
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?, ?, ?, ?);        
                """
    
                params = (student_id, act_id, params[2], params[3], params[4], params[-1])
            else:
                return False
            


        elif self._tblname == 'student_cca':
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False
            student_id = student_data[0]

            cca = 'CCA'
            VIEW = f"""
                SELECT * FROM {cca} 
                WHERE "Name"=?;
            """
            val = (params[1], )
            c.execute(VIEW, val)
            cca_data = c.fetchone()
            if cca_data == None:
                return False
            cca_id = cca_data[0]


            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "student_id"=? AND "cca_id"=?;
            """
            val = (student_id, cca_id)
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:

                QUERY = f"""
                    INSERT INTO {self._tblname} 
                    VALUES (?, ?, ?);        
                """
    
                params = (student_id, cca_id, params[-1])
            else:
                return False
                
        c.execute(QUERY, params)
        conn.commit()
        conn.close()
        return True



    
    
    def add_id(self):
        data = self.view_all()
        num = len(data)
        return num + 1




    
    def view_record(self, record):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        details = list(record.values())
        if self._tblname == 'student_class':
            name = details[0]
            student = 'Student'
            VIEW = f"""
            SELECT * FROM {student} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return None

            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "student_id"=?;
            """
            val = (student_data[0], )
            c.execute(VIEW, val)
            studentclass_data = c.fetchone()
            if studentclass_data == None:
                return None
            
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


        elif self._tblname == 'cca_activity':
            name = details[0]
            cca = 'CCA'
            VIEW = f"""
            SELECT * FROM {cca} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            cca_data = c.fetchone()
            if cca_data == None:
                return None

            act = 'Activity'
            VIEW = f"""
            SELECT * FROM {act} 
            WHERE "Name"=?;
            """
            val = (details[1], )
            c.execute(VIEW, val)
            act_data = c.fetchone()
            if act_data == None:
                return None

            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "cca_id"=? AND "activity_id"=?;
            """
            val = (cca_data[0], act_data[0])
            c.execute(VIEW, val)
            ccaact_data = c.fetchone()

            if ccaact_data == None:
                return None
            

            conn.commit()
            conn.close()
            return (cca_data[1], act_data[1])



        elif self._tblname == 'student_activity':
            name = details[0]
            student = 'Student'
            VIEW = f"""
            SELECT * FROM {student} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return None

            act = 'Activity'
            VIEW = f"""
            SELECT * FROM {act} 
            WHERE "Name"=?;
            """
            val = (details[1], )
            c.execute(VIEW, val)
            act_data = c.fetchone()
            if act_data == None:
                return None
            
            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "student_id"=? AND "activity_id"=?;
            """
            val = (student_data[0], act_data[0])
            c.execute(VIEW, val)
            studentact_data = c.fetchone()
            if studentact_data == None:
                return None

            

            conn.commit()
            conn.close()
            return (student_data[1], act_data[1], studentact_data[2], studentact_data[3], studentact_data[4], studentact_data[5])

        
        elif self._tblname == 'student_cca':
            name = details[0]
            student = 'Student'
            VIEW = f"""
            SELECT * FROM {student} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            
            if student_data == None:
                return None

            cca = 'CCA'
            VIEW = f"""
            SELECT * FROM {cca} 
            WHERE "Name"=?;
            """
            val = (details[1], )
            c.execute(VIEW, val)
            cca_data = c.fetchone()
            if cca_data == None:
                return None
                
            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "student_id"=? AND "cca_id"=?;
            """
            val = (student_data[0], cca_data[0])
            c.execute(VIEW, val)
            studentcca_data = c.fetchone()

            if studentcca_data == None:
                return None
            

            conn.commit()
            conn.close()
            return (student_data[1], cca_data[1], studentcca_data[-1])


        elif self._tblname == 'student_subject':
            name = details[0]
            student = 'Student'
            VIEW = f"""
            SELECT * FROM {student} 
            WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            
            if student_data == None:
                return None

            sub = 'Subjects'
            VIEW = f"""
            SELECT * FROM {sub} 
            WHERE "Name"=? AND "Level"=?;
            """
            val = (details[1], details[-1])
            c.execute(VIEW, val)
            sub_data = c.fetchone()
            if sub_data == None:
                return None

            VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "student_id"=? AND "subject_id"=?;
            """
            val = (student_data[0], sub_data[0])
            c.execute(VIEW, val)
            studentsub_data = c.fetchone()

            if studentsub_data == None:
                return None

            conn.commit()
            conn.close()
            return (student_data[1], sub_data[1], sub_data[-1])

        elif self._tblname == 'Subjects':
            name = details[0]
            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "Name"=? AND "Level"=?;
            """
            val = (name, details[1])
            c.execute(VIEW, val)
            result = c.fetchone()
            if result == None:
                return result
    
            
            conn.commit()
            conn.close()
            result = list(result)
            result.pop(0)
            result = tuple(result)
            return result
            
        
        name = details[0]
        VIEW = f"""
            SELECT * FROM {self._tblname} 
            WHERE "Name"=?;
        """
        val = (name,)
        c.execute(VIEW, val)
        result = c.fetchone()
        if result == None:
            return result

        
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



        elif self._tblname == 'cca_activity':
            
            data = []
            for x in result:
                
                cca = 'CCA'
                VIEW = f"""
                SELECT * FROM {cca} 
                WHERE "id"=?;
                """
                val = (x[0], )
                c.execute(VIEW, val)
                cca_data = c.fetchone()
    
                act = 'Activity'
                VIEW = f"""
                SELECT * FROM {act} 
                WHERE "id"=?;
                """
                val = (x[1], )
                c.execute(VIEW, val)
                act_data = c.fetchone()

                data.append((cca_data[1], act_data[1]))

            conn.close()
            return data



        elif self._tblname == 'student_activity':
            
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
    
                act = 'Activity'
                VIEW = f"""
                SELECT * FROM {act} 
                WHERE "id"=?;
                """
                val = (x[1], )
                c.execute(VIEW, val)
                act_data = c.fetchone()

                data.append((student_data[1], act_data[1], x[2], x[3], x[4], x[5]))

            conn.close()
            return data



        elif self._tblname == 'student_subject':
            
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
    
                sub = 'Subjects'
                VIEW = f"""
                SELECT * FROM {sub} 
                WHERE "id"=?;
                """
                val = (x[1], )
                c.execute(VIEW, val)
                sub_data = c.fetchone()

                data.append((student_data[1], sub_data[1], sub_data[2]))

            conn.close()
            return data


        elif self._tblname == 'student_cca':
            
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
    
                cca = 'CCA'
                VIEW = f"""
                SELECT * FROM {cca} 
                WHERE "id"=?;
                """
                val = (x[1], )
                c.execute(VIEW, val)
                cca_data = c.fetchone()

                data.append((student_data[1], cca_data[1], x[-1]))

            conn.close()
            return data
                
            
        for i, x in enumerate(result):
            x = list(x)
            x.pop(0)
            x = tuple(x)
            result[i] = x

        conn.close()
        return result
        

    

    def edit_record(self, old_record, new_record):      
        old_details = list(old_record.values())
        new_details = list(new_record.values())
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        
        if self._tblname == 'CCA':
            name = old_details[0]
            check = self.view_record(name)
            if check == None:
                return False
            data = self.view_all()
            id = data.index(check) + 1
            query = f"""UPDATE {self._tblname} 
                        SET "id" = ?,
                            "Name" = ?,
                            "Type" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, new_details[0], new_details[1], name)

        elif self._tblname == 'Class':
            name = old_details[0]
            check = self.view_record(name)
            if check == None:
                return False
            data = self.view_all()
            id = data.index(check) + 1
            query = f"""UPDATE {self._tblname} 
                        SET "id" = ?,
                            "Name" = ?,
                            "Level" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, new_details[0], new_details[1], name)
            
        elif self._tblname == 'Activity':
            name = old_details[0]
            check = self.view_record(name)
            if check == None:
                return False
            data = self.view_all()
            id = data.index(check) + 1
            query = f"""UPDATE {self._tblname}
                        SET "id" = ?,
                            "Name" = ?,
                            "Description" = ?,
                            "Start_Date" = ?,
                            "End_Date" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, new_details[0], new_details[1], new_details[2], new_details[3], name)

        elif self._tblname == 'Student':
            name = old_details[0]
            check = self.view_record(name)
            if check == None:
                return False
            data = self.view_all()
            id = data.index(check) + 1
            query = f"""UPDATE {self._tblname}
                        SET "id" = ?,
                            "Name" = ?,
                            "Age" = ?,
                            "Year_Enrolled" = ?,
                            "Graduating_Year" = ?
                        WHERE "Name" = ?
                        ;"""
            val = (id, new_details[0], new_details[1], new_details[2], new_details[3], name)

        elif self._tblname == 'Subjects':
            CHECK = f"""SELECT * FROM {self._tblname}
                        WHERE "Name"=? AND "Level"=?;"""
            val = (old_details[0], old_details[1])
            c.execute(CHECK, val)
            check = c.fetchone()
            if check == None:
                return False

            CHECK = f"""SELECT * FROM {self._tblname}
                        WHERE "Name"=? AND "Level"=?;"""
            val = (new_details[0], new_details[1])
            c.execute(CHECK, val)
            check2 = c.fetchone()
            data = self.view_all()
            check = list(check)
            s = check.pop(0)
            check = tuple(check)
            id = data.index(check) + 1
            if old_record == new_record:
                query = f"""UPDATE {self._tblname} 
                            SET "id" = ?,
                                "Name" = ?,
                                "Level" = ?
                            WHERE "Name" = ? AND "Level" = ?
                            ;"""
                val = (id, new_details[0], new_details[1], old_details[0], old_details[1])
                
            elif check2 == None:

                query = f"""UPDATE {self._tblname} 
                            SET "id" = ?,
                                "Name" = ?,
                                "Level" = ?
                            WHERE "Name" = ? AND "Level" = ?
                            ;"""
                val = (check[0], new_details[0], new_details[1], old_details[0], old_details[1])
            else:
                return False


        elif self._tblname == 'student_class':
            name = old_details[0]
            student = 'Student'
            VIEW = f"""SELECT * FROM {student} 
                        WHERE "Name" = ?;"""
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False
                

            VIEW = f"""SELECT * FROM {self._tblname}
                    WHERE "student_id"=?;"""
            val = (student_data[0], )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return False

            theclass = 'Class'
            VIEW = f"""SELECT * FROM {theclass} 
                        WHERE "Name" = ?;"""
            val = (new_details[-1], )
            c.execute(VIEW, val)
            class_data = c.fetchone()
            if class_data == None:
                return False
            query = f"""UPDATE {self._tblname} 
                        SET "student_id" = ?,
                            "class_id" = ?
                        WHERE "student_id" = ?
                        ;"""
            val = (student_data[0], class_data[0], student_data[0])



        elif self._tblname == 'cca_activity':
            name = old_details[0]
            cca = 'CCA'
            VIEW = f"""SELECT * FROM {cca} 
                        WHERE "Name" = ?;"""
            val = (name, )
            c.execute(VIEW, val)
            cca_data = c.fetchone()
            if cca_data == None:
                return False

            act = 'Activity'
            VIEW = f"""SELECT * FROM {act} 
                        WHERE "Name" = ?;"""
            val = (old_details[-1], )
            c.execute(VIEW, val)
            oldact_data = c.fetchone()
            if oldact_data == None:
                return False

            VIEW = f"""SELECT * FROM {act} 
                        WHERE "Name" = ?;"""
            val = (new_details[-1], )
            c.execute(VIEW, val)
            newact_data = c.fetchone()
            if newact_data == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "cca_id" = ? AND "activity_id"=?;"""
            val = (cca_data[0], oldact_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "cca_id" = ? AND "activity_id"=?;"""
            val = (cca_data[0], newact_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check != None:
                return False
            query = f"""UPDATE {self._tblname} 
                        SET "cca_id" = ?,
                            "activity_id" = ?
                        WHERE "cca_id" = ? AND "activity_id"=?
                        ;"""
            val = (cca_data[0], newact_data[0], cca_data[0], oldact_data[0])


        elif self._tblname == 'student_activity':
            name = old_details[0]
            student = 'Student'
            VIEW = f"""SELECT * FROM {student} 
                        WHERE "Name" = ?;"""
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False

            act = 'Activity'
            VIEW = f"""SELECT * FROM {act} 
                        WHERE "Name" = ?;"""
            val = (old_details[1], )
            c.execute(VIEW, val)
            oldact_data = c.fetchone()
            if oldact_data == None:
                return False
            
            VIEW = f"""SELECT * FROM {act} 
                        WHERE "Name" = ?;"""
            val = (new_details[0], )
            c.execute(VIEW, val)
            newact_data = c.fetchone()
            if newact_data == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "student_id" = ? AND "activity_id"=?;"""
            val = (student_data[0], oldact_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "student_id" = ? AND "activity_id"=?;"""
            val = (student_data[0], newact_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check != None:
                return False
            query = f"""UPDATE {self._tblname} 
                        SET "student_id" = ?,
                            "activity_id" = ?,
                            "Role" = ?,
                            "Category" = ?,
                            "Award" = ?,
                            "Hours" = ?
                        WHERE "student_id" = ? AND "activity_id"=?
                        ;"""
            val = (student_data[0], newact_data[0], new_details[1], new_details[2], new_details[3], new_details[4], student_data[0], oldact_data[0])


        elif self._tblname == 'student_subject':
            name = old_details[0]
            student = 'Student'
            VIEW = f"""SELECT * FROM {student} 
                        WHERE "Name" = ?;"""
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False


            sub = 'Subjects'
            VIEW = f"""SELECT * FROM {sub} 
                        WHERE "Name" = ? AND "Level" = ?;"""
            val = (old_details[1], old_details[2])
            c.execute(VIEW, val)
            oldsub_data = c.fetchone()
            if oldsub_data == None:
                return False

            VIEW = f"""SELECT * FROM {sub} 
                        WHERE "Name" = ? AND "Level" = ?;"""
            val = (new_details[0], new_details[1])
            c.execute(VIEW, val)
            newsub_data = c.fetchone()
            if newsub_data == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "student_id" = ? AND "subject_id" = ?;"""
            val = (student_data[0], oldsub_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return False
            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "student_id" = ? AND "subject_id" = ?;"""
            val = (student_data[0], newsub_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check != None:
                return False
            query = f"""UPDATE {self._tblname} 
                        SET "student_id" = ?,
                            "subject_id" = ?
                        WHERE "student_id" = ? AND "subject_id" = ?
                        ;"""
            val = (student_data[0], newsub_data[0], student_data[0], oldsub_data[0])


        elif self._tblname == 'student_cca':
            name = old_details[0]
            student = 'Student'
            VIEW = f"""SELECT * FROM {student} 
                        WHERE "Name" = ?;"""
            val = (name, )
            c.execute(VIEW, val)
            student_data = c.fetchone()
            if student_data == None:
                return False

            cca = 'CCA'
            VIEW = f"""SELECT * FROM {cca} 
                        WHERE "Name" = ?;"""
            val = (old_details[1], )
            c.execute(VIEW, val)
            oldcca_data = c.fetchone()
            if oldcca_data == None:
                return False
                
            VIEW = f"""SELECT * FROM {cca} 
                        WHERE "Name" = ?;"""
            val = (new_details[0], )
            c.execute(VIEW, val)
            newcca_data = c.fetchone()
            if newcca_data == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "student_id" = ? AND "cca_id" = ?;"""
            val = (student_data[0], oldcca_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return False

            VIEW = f"""SELECT * FROM {self._tblname} 
                        WHERE "student_id" = ? AND "cca_id" = ?;"""
            val = (student_data[0], newcca_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check != None:
                return False
            query = f"""UPDATE {self._tblname} 
                        SET "student_id" = ?,
                            "cca_id" = ?,
                            "Role" = ?
                        WHERE "student_id" = ? AND "cca_id" = ?
                        ;"""
            val = (student_data[0], newcca_data[0], new_details[-1], student_data[0], oldcca_data[0])
            
        c.execute(query, val)
        conn.commit()
        conn.close()
        return True


    def delete_record(self, record):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        details = list(record.values())
        name = details[0]
        
        if self._tblname == 'Subjects':
            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "Name"=? AND "Level"=?;
            """
            val = (name, details[1])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such subject exists.'
            subject_data = check
            
            query = f"""
                    DELETE FROM {self._tblname}
                    WHERE "Name" = ? AND "Level" = ?;
                    """
            val = (name, details[1])
            c.execute(query, val)

            ss = 'student_subject'
            query = f"""
                    DELETE FROM {ss}
                    WHERE "subject_id" = ?;
                    """
            val = (subject_data[0], )
            c.execute(query, val)

            self.reorder()
            conn.commit()
            conn.close()
            
            
        elif self._tblname == 'CCA':
            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            data = c.fetchone()
            if data == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname} 
                    WHERE "Name"=?;
                """
            val = (name, )
            c.execute(DEL, val)
            
            sc = 'student_cca'
            ca = 'cca_activity'
            query = f"""
            DELETE FROM {sc}
            WHERE "cca_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            
            query = f"""
            DELETE FROM {ca}
            WHERE "cca_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            conn.commit()
            conn.close()
            self.reorder()

        elif self._tblname == 'Activity':
            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            data = c.fetchone()
            if data == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname} 
                    WHERE "Name"=?;
                """
            val = (name, )
            c.execute(DEL, val)
            
            sa = 'student_activity'
            ca = 'cca_activity'
            query = f"""
            DELETE FROM {sa}
            WHERE "activity_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            
            query = f"""
            DELETE FROM {ca}
            WHERE "activity_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            conn.commit()
            conn.close()
            self.reorder()


        elif self._tblname == 'Student':
            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            data = c.fetchone()
            if data == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname} 
                    WHERE "Name"=?;
                """
            val = (name, )
            c.execute(DEL, val)
            
            sa = 'student_activity'
            ss = 'student_subject'
            sc = 'student_cca'
            scla = 'student_class'
            
            query = f"""
            DELETE FROM {sa}
            WHERE "student_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            
            query = f"""
            DELETE FROM {sc}
            WHERE "student_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)

            query = f"""
            DELETE FROM {ss}
            WHERE "student_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            
            query = f"""
            DELETE FROM {scla}
            WHERE "student_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            
            conn.commit()
            conn.close()
            self.reorder()

        elif self._tblname == 'Class':
            VIEW = f"""
                SELECT * FROM {self._tblname} 
                WHERE "Name"=?;
            """
            val = (name, )
            c.execute(VIEW, val)
            data = c.fetchone()
            if data == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname} 
                    WHERE "Name"=?;
                """
            val = (name, )
            c.execute(DEL, val)
            
            sc = 'student_class'
            query = f"""
            DELETE FROM {sc}
            WHERE "class_id" = ?;
            """
            val = (data[0], )
            c.execute(query, val)
            conn.commit()
            conn.close()
            self.reorder()

        elif self._tblname == 'student_subject':
            student_name = details[0]
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (student_name, )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such student exists.'
            student_data = check

            sub = 'Subjects'
            VIEW = f"""
                    SELECT * FROM {sub}
                    WHERE "Name" = ? AND "Level" = ?;
                    """
            val = (details[1], details[2])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such subject exists.'
            subject_data = check

            VIEW = f"""
                    SELECT * FROM {self._tblname}
                    WHERE "student_id" = ? AND "subject_id" = ?;
                    """
            val = (student_data[0], subject_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'That student does not even take that subject.'
                
            DEL = f"""
                    DELETE FROM {self._tblname}
                    WHERE "student_id" = ? AND "subject_id" = ?;
                    """
            val = (student_data[0], subject_data[0])
            c.execute(DEL, val)
            conn.commit()
            conn.close()

        elif self._tblname == 'student_class':
            student_name = details[0]
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (student_name, )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            student_data = check

            cla = 'Class'
            VIEW = f"""
                    SELECT * FROM {cla}
                    WHERE "Name" = ?;
                    """
            val = (details[1], )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            class_data = check

            VIEW = f"""
                    SELECT * FROM {self._tblname}
                    WHERE "student_id" = ? AND "class_id" = ?;
                    """
            val = (student_data[0], class_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname}
                    WHERE "student_id" = ? AND "class_id" = ?;
                    """
            val = (student_data[0], class_data[0])
            c.execute(DEL, val)
            conn.commit()
            conn.close()


        elif self._tblname == 'student_cca':
            student_name = details[0]
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (student_name, )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            student_data = check

            cca = 'CCA'
            VIEW = f"""
                    SELECT * FROM {cca}
                    WHERE "Name" = ?;
                    """
            val = (details[1], )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            cca_data = check

            VIEW = f"""
                    SELECT * FROM {self._tblname}
                    WHERE "student_id" = ? AND "cca_id" = ?;
                    """
            val = (student_data[0], cca_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname}
                    WHERE "student_id" = ? AND "cca_id" = ?;
                    """
            val = (student_data[0], cca_data[0])
            c.execute(DEL, val)
            conn.commit()
            conn.close()


        elif self._tblname == 'student_activity':
            student_name = details[0]
            student = 'Student'
            VIEW = f"""
                SELECT * FROM {student} 
                WHERE "Name"=?;
            """
            val = (student_name, )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            student_data = check

            a = 'Activity'
            VIEW = f"""
                    SELECT * FROM {a}
                    WHERE "Name" = ?;
                    """
            val = (details[1], )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            act_data = check

            VIEW = f"""
                    SELECT * FROM {self._tblname}
                    WHERE "student_id" = ? AND "activity_id" = ?;
                    """
            val = (student_data[0], act_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname}
                    WHERE "student_id" = ? AND "activity_id" = ?;
                    """
            val = (student_data[0], act_data[0])
            c.execute(DEL, val)
            conn.commit()
            conn.close()


        elif self._tblname == 'cca_activity':
            cca_name = details[0]
            cca = 'CCA'
            VIEW = f"""
                SELECT * FROM {cca} 
                WHERE "Name"=?;
            """
            val = (cca_name, )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            cca_data = check

            a = 'Activity'
            VIEW = f"""
                    SELECT * FROM {a}
                    WHERE "Name" = ?;
                    """
            val = (details[1], )
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
            act_data = check

            VIEW = f"""
                    SELECT * FROM {self._tblname}
                    WHERE "cca_id" = ? AND "activity_id" = ?;
                    """
            val = (cca_data[0], act_data[0])
            c.execute(VIEW, val)
            check = c.fetchone()
            if check == None:
                return 'No such record exists.'
                
            DEL = f"""
                    DELETE FROM {self._tblname}
                    WHERE "cca_id" = ? AND "activity_id" = ?;
                    """
            val = (cca_data[0], act_data[0])
            c.execute(DEL, val)
            conn.commit()
            conn.close()


        
    

    

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
                self.edit_record(temp, temp)
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

class StudentCCACollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'student_cca')

class StudentActivityCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'student_activity')

class StudentSubjectCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'student_subject')

class CCAActivityCollection(Collection):
    def __init__(self):
        super().__init__('capstoneV6.db', 'cca_activity')
