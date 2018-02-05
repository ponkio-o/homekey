#coding:utf-8
import nfc
import binascii
import RPi.GPIO as GPIO
import time
import MySQLdb
import wiringpi

#リードスイッチの設定
readswitch_pin = 3
wiringpi.wiringPiSetupGpio()

#施錠解錠処理
def check():
    c = connect.cursor()
    sql = "select * from member"
    c.execute(sql)
    for row in c.fetchall():
        if(row[1] == idm):
            print "Unlock!"
            unlock()
            log()
            print "Wait..."
            while True:
                if( wiringpi.digitalRead(readswitch_pin) == 0 ):
                    time.sleep(5)
                    lock()
                    break
                else:
                    None
            print "Lock!"
    c.close()

#ログ記録
def log():
    c = connect.cursor()
    sql = "insert into access_log values (%s,%s)"
    c.execute(sql,(idm,None))
    connect.commit()
    c.close()

#解錠
def unlock():
    GPIO.setmode(GPIO.BCM)
    gp_out = 18
    GPIO.setup(gp_out, GPIO.OUT)
    servo = GPIO.PWM(gp_out, 50)
    servo.start(0.0)
    servo.ChangeDutyCycle(7.0)
    time.sleep(0.5)
    GPIO.cleanup()

#施錠
def lock():
    GPIO.setmode(GPIO.BCM)
    gp_out = 18
    GPIO.setup(gp_out, GPIO.OUT)
    servo = GPIO.PWM(gp_out, 50)
    servo.start(0.0)
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    GPIO.cleanup()

#カード読み取り
def read():
    def connected(tag):
        global idm
        idm = binascii.hexlify(tag.idm)
    clf = nfc.ContactlessFrontend('usb')
    clf.connect(rdwr={'on-connect': connected}) # now touch a tag
    clf.close()


print "Weclome back."
while True:
    print "Please touch a card."

    #MySQL接続
    connect = MySQLdb.connect(user="user",passwd="password",host="your host",db="felica")
    read()
    check()
    connect.close()
