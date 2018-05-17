#!/usr/bin/env Python
# coding=utf-8
import mysql.connector
# conn = mysql.connector.connect(host="localhost", user="root", passwd="zv63108412", db="grave_server_db", port=3306, charset="utf8")    #连接对象
conn = mysql.connector.connect(host="35.229.220.81", user="root", passwd="zv63108412", db="detector", port=3306, charset="utf8")
cur = conn.cursor()    #游标对象

def select_user(user_name):
    sql = "select * from user where user_name = \'"+user_name+"\'"
    cur.execute(sql)
    return cur.fetchone()

def update_user_device(user_name, deviceIds):
    sql = "update user set deviceIds = %s where user_name = %s"
    cur.execute(sql, (deviceIds, user_name))
    conn.commit()

def bind_user(user_name, deviceIds):
    sql = "insert into user(user_name, deviceIds) values (%s, %s)"
    cur.execute(sql, (user_name, deviceIds))
    conn.commit()

def add_device(deviceName):
    sql = "insert into device (deviceName) values(\'"+deviceName+"\')"
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def select_deviceName(deviceId):
    sql = "select * from device where deviceId = "+deviceId
    cur.execute(sql)
    return cur.fetchone()

def update_balance(user_name,balance):
    sql = "update user set balance = %s where user_name = %s"
    cur.execute(sql, (balance, user_name))
    conn.commit()