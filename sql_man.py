#!/usr/bin/python
#-*- coding: utf-8 -*-

import sqlite3 as lite
import sys


class sql_man(object):
    def __init__(self):
        self.con = lite.connect('data/speziinvest.db')

    def check(self, user_id):
        with self.con:
            cur = self.con.cursor()
            uid = int(user_id)
            cur.execute('SELECT count(1) FROM users WHERE uid = ?;', (uid,))
            return int(cur.fetchone()[0])

    def read(self, user_id):
        with self.con:
            cur = self.con.cursor()
            uid = int(user_id)
            #get user
            cur.execute('SELECT name FROM users WHERE uid=?', (uid,))
            user = str(cur.fetchone()[0])
            # deduct money from credit
            cur.execute('SELECT credit FROM users WHERE uid=?', (uid,))
            credit = float(cur.fetchone()[0])
            return [user, credit]
        return ["Error occured", 0]
            
    def book(self,item, user_id):
        with self.con:
            cur = self.con.cursor()
            iid = int(item)
            uid = int(user_id)
            #get user
            cur.execute('SELECT name FROM users WHERE uid=?', (uid,))
            user = str(cur.fetchone()[0])
            # get price
            cur.execute('SELECT price FROM store WHERE id=?', (iid,))
            price = float(cur.fetchone()[0])
            # deduct money from credit
            cur.execute('SELECT credit FROM users WHERE uid=?', (uid,))
            credit = float(cur.fetchone()[0])
            diff = str(credit - price)
            cur.execute('UPDATE users SET credit=? WHERE uid=?', (diff, uid,))
            # increase counter by one
            cur.execute('SELECT item FROM store WHERE id=?', (iid,))
            name = "n_" + str(cur.fetchone()[0]).lower()
            cur.execute('SELECT %s FROM users WHERE uid=?'%name,(uid,))
            new_amount = int(cur.fetchone()[0]) + 1
            cur.execute('UPDATE users SET %s=? WHERE uid=?'%name, (new_amount, uid,))
            return [user, diff]
        return ["Error occured in database communication.", 0]
