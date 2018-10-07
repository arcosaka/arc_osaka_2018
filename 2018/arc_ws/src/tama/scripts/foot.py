#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reference:https://karaage.hatenadiary.jp/entry/2017/02/10/073000
Summery: Move servo angle to the topic value 'servo_angle'
"""

import pigpio
import rospy
from tama.msg import foot
from param import Direction
from param import Speed
# defined const

# pin number
PIN_AIN1    = 26    # GPIO.25 Left IN1
PIN_AIN2    = 19    # GPIO.24 Left IN2
PIN_PWMA    = 13    # GPIO.23 Left PWM
PIN_BIN1    = 20    # GPIO.28 Right IN1
PIN_BIN2    = 16    # GPIO.27 Right IN2
PIN_PWMB    = 12    # GPIO.26 Right PWM

HIGHSPD     = 255   # 速度：高
MEDIUMSPD   = 192   # 速度：中
LOWSPD      = 128   # 速度：低

HIGH        = 1     # 定数
LOW         = 0     # 定数

# initialize gpio
pi = pigpio.pi()
pi.set_mode(PIN_AIN1, pigpio.OUTPUT)
pi.set_mode(PIN_AIN2, pigpio.OUTPUT)
pi.set_mode(PIN_PWMA, pigpio.OUTPUT)
pi.set_mode(PIN_BIN1, pigpio.OUTPUT)
pi.set_mode(PIN_BIN2, pigpio.OUTPUT)
pi.set_mode(PIN_PWMB, pigpio.OUTPUT)

def callback(foot):
    #Comment out
    #duty = ((foot.frame_id + 90.) / 180. * 1.9 + 0.5)\
    #        / 20. * 1e6
    #pi.hardware_PWM(pwm_pin, 50, int(0))
    print("frame_id = %d" % foot.frame_id)
    print("direction = %d" % foot.direction)
    print("speed = %d" % foot.speed)
    print"==============="

    #方向制御
    #前進
    if foot.direction == Direction.AHEAD:
        output_direction(LOW, HIGH, HIGH, LOW)      # Left Motor : CCW, Right Motor : CW

    #後進
    elif foot.direction == Direction.BACK:
        output_direction(HIGH, LOW, LOW, HIGH)      # Left Motor : CW, Right Motor : CCW

    #右旋回
    elif foot.direction == Direction.RIGHT:
        output_direction(LOW, HIGH, LOW, HIGH)      # Left Motor : CCW, Right Motor : CCW

    #左旋回
    elif foot.direction == Direction.LEFT:
        output_direction(HIGH, LOW, HIGH, LOW)      # Left Motor : CW, Right Motor : CW

    #停止
    elif foot.direction == Direction.STOP:
        output_direction(HIGH, HIGH, HIGH, HIGH)    # Left Motor : ShortBreak, Right Motor : ShortBreak
    else:
        pass


    #速度制御
    if foot.speed == Speed.HIGH:
        output_pwm(HIGHSPD)         # 速度：高

    elif foot.speed == Speed.MIDDLE:
        output_pwm(MEDIUMSPD)       # 速度：中

    elif foot.speed == Speed.LOW:
        output_pwm(LOWSPD)          # 速度：低

    else:
        pass

def output_pwm(SPD):                        # PWM Duty比
    pi.set_PWM_dutycycle(PIN_PWMA, SPD)
    pi.set_PWM_dutycycle(PIN_PWMB, SPD)

def output_direction(AIN1, AIN2, BIN1, BIN2):   # 方向
    #Left Motor
    pi.write(PIN_AIN1,AIN1)
    pi.write(PIN_AIN2,AIN2)
    #Right Motor
    pi.write(PIN_BIN1,BIN1)
    pi.write(PIN_BIN2,BIN2)

def foot_py():
    rospy.init_node('foot_py_node',anonymous=True)
    sub=rospy.Subscriber('foot', foot, callback, queue_size=1)
    print "start"
    rospy.spin()

if __name__ == '__main__':
   foot_py()