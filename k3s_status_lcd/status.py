#!/usr/bin/python3
"""
Render k3s cluster stats on a LCD display
"""

import os
import time
import struct
import socket
import fcntl
import i2c_lcd

from kubernetes import client, config

DISPLAY_DELAY = 10

try:
    config.load_kube_config(os.path.join(os.environ["HOME"], '.kube/config'))
except Exception as err:
    print(err)

kube_cli = client.CoreV1Api()
lcd = i2c_lcd.lcd()

def print_welcome():
    lcd.lcd_clear()
    lcd.lcd_display_string('k3s lcd status svc', 1)
    lcd.lcd_display_string('running ^_^', 2)

def print_k3s_overview():
    lcd.lcd_clear()
    lcd.lcd_display_string('k3s status', 1)
    lcd.lcd_display_string('nodes: 3', 2)
    lcd.lcd_display_string('pods: 8', 3)

if __name__ == "__main__":
    print("starting service")
    try:
        print("printing welcome message")
        print_welcome()
        time.sleep(DISPLAY_DELAY)
        
        while True:
            print("printing k3s overview")
            print_k3s_overview()
            time.sleep(DISPLAY_DELAY)

            print("printing welcome message")
            print_welcome()
            time.sleep(DISPLAY_DELAY)
    except KeyboardInterrupt:
        pass