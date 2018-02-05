#coding:utf-8
import nfc
import binascii
import RPi.GPIO as GPIO
import time
import wiringpi

button_pin = 2
readswitch_pin = 3
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode( button_pin, 0 )
wiringpi.pullUpDnControl( button_pin, 2 )
wiringpi.pullUpDnControl( button_pin, 3 )

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

while True:
    #ボタンが押されたら解錠する
    if( wiringpi.digitalRead(button_pin) == 0 ):
        None
    else:
        unlock()
        time.sleep(5)
        while True:
            #ドアが閉まったら施錠する
            if( wiringpi.digitalRead(readswitch_pin) == 0 ):
                time.sleep(5)
                lock()
                break
            else:
                None
