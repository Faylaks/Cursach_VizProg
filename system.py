import sys, sqlite3
from datetime import datetime
from myglobal import *

def setChangeDate(cursor, journalId):
        q = f"""UPDATE journal SET change_date = {int(datetime.timestamp(datetime.now()))} WHERE id = {journalId}"""
        cursor.execute(q)
do = {"createJournal": 1, 
      "deleteJournal": 2, 
      "createEvent": 3, 
      "createUser": 6, 
      "createType": 8, 
      "deleteEvent": 12, 
      "deleteType": 21, 
      "clearEvent": 30,}

def createJournalLog(cursor, userId, journalId):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["createJournal"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}")"""
        cursor.execute(q)
def createUserLog(cursor, userId):
        setChangeDate(cursor, systemJournalId)
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["createUser"]}, {int(datetime.timestamp(datetime.now()))}, "---")"""
        cursor.execute(q)
def createTypelLog(cursor, userId, journalId, typeName):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["createType"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}->{typeName}")"""
        cursor.execute(q)
def createEventlLog(cursor, userId, journalId, typeName):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["createEvent"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}->{typeName}")"""
        cursor.execute(q)
def deleteEventLog(cursor, userId, journalId, typeName):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["deleteEvent"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}->{typeName}")"""
        cursor.execute(q)
def deleteTypeLog(cursor, userId, journalId, typeName):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["deleteType"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}->{typeName}")"""
        cursor.execute(q)
def clearEventLog(cursor, userId, journalId):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["clearEvent"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}")"""
        cursor.execute(q)
def deleteJournalLog(cursor, userId, journalId):
        setChangeDate(cursor, systemJournalId)
        q = f"""SELECT name FROM journal WHERE id = {journalId}"""
        cursor.execute(q)
        journalName = cursor.fetchone()[0]
        q = f"""INSERT INTO log (user_id, journal_id, type_id, date, external) 
                VALUES({userId}, {systemJournalId}, {do["deleteJournal"]}, {int(datetime.timestamp(datetime.now()))}, "{journalName}")"""
        cursor.execute(q)


