from datetime import datetime, timezone, timedelta
from os import path
import mydb

def getUserName(did):
    with mydb.db_cursor() as cur:
        cur.execute("SELECT name from users where did = %s", (did,))
        return cur.fetchone()

def getCardsInSetByName(name):
    with mydb.db_cursor() as cur:
        cur.execute("SELECT monid, mons.name from cardsinsets join mons on cardsinsets.monid = mons.rwid join"+
                    " sets on cardsinsets.setid = sets.rwid where sets.name = %s", (name,))
        return cur.fetchall()

def getBaseSetCards():
    with mydb.db_cursor() as cur:
        cur.execute("SELECT monid, mons.name from cardsinsets join mons on cardsinsets.monid = mons.rwid join"+
                    " sets on cardsinsets.setid = sets.rwid where sets.rwid <= 0")
        return cur.fetchall()

def getMonSets():
    with mydb.db_cursor() as cur:
        cur.execute("SELECT name from sets where rwid > 0 and rwid <50")
        return cur.fetchall()

def getItemSets():
    with mydb.db_cursor() as cur:
        cur.execute("SELECT name from sets where rwid >= 50 and rwid <99")
        return cur.fetchall()

def getLocSets():
    with mydb.db_cursor() as cur:
        cur.execute("SELECT name from sets where rwid >= 300 and rwid <400")
        return cur.fetchall()

def getExpansions():
    with mydb.db_cursor() as cur:
        cur.execute("select exp,expansion from expansions join sets on expansions.expansion = sets.name order by sets.rwid")
        return cur.fetchall()

def getAllCollections():
    with mydb.db_cursor() as cur:
        cur.execute("select users.name, collections.rwid, mons.cr, mons.name, mons.exp, grade, holo, ed, value, c.name from"+
                " collections inner join users on collections.uid = users.rwid inner join mons on collections.monid = mons.rwid"+
                " left join (select monid, setid, name from cardsinsets inner join sets on sets.rwid = cardsinsets.setid"+
                " where sets.rwid > 0) as c on c.monid = collections.monid")
        return cur.fetchall()

def getCardsForUser(user,c):
    with mydb.db_cursor() as cur:
        cur.execute("select collections.rwid, mons.cr, mons.name, mons.exp, grade, holo, ed, value, collections.date, mons.rwid, c.name"+
                " from collections inner join users on collections.uid = users.rwid inner join mons on collections.monid = mons.rwid"+
                " left join (select monid, setid, name from cardsinsets inner join sets on sets.rwid = cardsinsets.setid"+
                " where sets.rwid > 0) as c on c.monid = collections.monid where users.did = %s and mons.name like %s",(user,'%(#' + c +')%'))
        return cur.fetchall()

def getFullCollection(user):
    with mydb.db_cursor() as cur:
        cur.execute("select collections.rwid, mons.cr, mons.name, mons.exp, grade, holo, ed, value, collections.date, mons.rwid, c.name"+
                    " from collections inner join users on collections.uid = users.rwid inner join mons on collections.monid = mons.rwid"+
                    " left join (select monid, setid, name from cardsinsets inner join sets on sets.rwid = cardsinsets.setid where"+
                    " sets.rwid > 0) as c on c.monid = collections.monid where users.did = %s",(user,))
        return cur.fetchall()

def getAllMonsters(user):
    with mydb.db_cursor() as cur:
        cur.execute("select collections.rwid, mons.cr, mons.name, mons.exp, grade, holo, ed, value, c.name from"+
                " collections inner join users on collections.uid = users.rwid inner join mons on collections.monid = mons.rwid"+
                " left join (select monid, setid, name from cardsinsets inner join sets on sets.rwid = cardsinsets.setid"+
                " where sets.rwid > 0) as c on c.monid = collections.monid where users.did = %s and mons.class = 'Monsters'",(user,))
        return cur.fetchall()

def getAllItems(user):
    with mydb.db_cursor() as cur:
        cur.execute("select collections.rwid, mons.cr, mons.name, mons.exp, grade, holo, ed, value, c.name from"+
                " collections inner join users on collections.uid = users.rwid inner join mons on collections.monid = mons.rwid"+
                " left join (select monid, setid, name from cardsinsets inner join sets on sets.rwid = cardsinsets.setid"+
                " where sets.rwid > 0) as c on c.monid = collections.monid where users.did = %s and mons.class = 'Item' ",(user,))
        return cur.fetchall()

def getAllLocations(user):
    with mydb.db_cursor() as cur:
        cur.execute("select collections.rwid, mons.cr, mons.name, mons.exp, grade, holo, ed, value, c.name from"+
                " collections inner join users on collections.uid = users.rwid inner join mons on collections.monid = mons.rwid"+
                " left join (select monid, setid, name from cardsinsets inner join sets on sets.rwid = cardsinsets.setid"+
                " where sets.rwid > 0) as c on c.monid = collections.monid where users.did = %s and mons.class = 'Locations'",(user,))
        return cur.fetchall()

def getAllUsers():
    with mydb.db_cursor() as cur:
        cur.execute("select name, did, count(value), sum(value), gp from users join collections on users.rwid = collections.uid"+
                    " group by (name, did, gp)")
        return cur.fetchall()

def setSession(ses, did):
    with mydb.db_cursor() as cur:
        cur.execute("insert into sessions values(%s, %s)", (ses, did))
    return

def getSession():
    with mydb.db_cursor() as cur:
        try:
            cur.execute("select did from sessions")
            return cur.fetchone()
        except:
            return None
