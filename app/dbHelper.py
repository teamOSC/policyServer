#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3,hashlib,time

class DB:
    conn = sqlite3.connect('data.db',check_same_thread=False)
    c = conn.cursor()

    def add_item(self,title, image_url,user_location,user_email,user_name):
        item_id = hashlib.md5(image_url+user_email).hexdigest()[:5]

        if item_id in self.exec_query("Select item_id from image_table"):
            print "Already present in DB"
            return item_id

        self.c.execute('''CREATE TABLE IF NOT EXISTS image_table
                     (item_id TEXT,title TEXT,image_url TEXT,user_location TEXT,user_email TEXT, user_name TEXT )''')
        self.c.execute("INSERT INTO image_table VALUES (?,?,?,?,?,?)",(item_id,title,image_url,user_location,user_email,user_name))
        self.conn.commit()
        return item_id

    def add_complaint(self,comp,location):
        item_id = hashlib.md5(comp+location).hexdigest()[:5]

        self.c.execute('''CREATE TABLE IF NOT EXISTS comp_table
                     (item_id TEXT,complaint TEXT,location TEXT)''')
        self.c.execute("INSERT INTO comp_table VALUES (?,?,?)",(item_id,comp,location))
        self.conn.commit()

    def add_bar(self,barcode,meta):
        item_id = hashlib.md5(barcode+meta).hexdigest()[:5]

        self.c.execute('''CREATE TABLE IF NOT EXISTS barcode_table
                     (item_id TEXT,barcode TEXT,meta TEXT)''')
        self.c.execute("INSERT INTO barcode_table VALUES (?,?,?)",(item_id,barcode,meta))
        self.conn.commit()

    def exec_query(self,query):
        try:
            result_arr = []
            self.c.execute(query)
            for row in self.c:
                result_arr.append(row)
            result_arr = [i[0] for i in result_arr]
            return result_arr
        except:
            return []

def test():
    D = DB()
    print D.exec_query("Select item_id from image_table")
    print D.add_item("Something","http://i.imgur.com/jtta7D2.jpg","Address","food@gmail.com","saurav")
    print D.add_complaint("Seeing lots of fake paracetamol medicines these days.",'Dehradun')
    print D.add_bar('123123b12h3b123','Panteen Bottle 2l')

if __name__ == '__main__':
    test()
