#!/usr/bin/python3
"""
Render k3s cluster stats on a LCD display
"""

import os
import time
import datetime
import i2c_lcd
import logging

from kubernetes import client, config

DISPLAY_DELAY = 10

try:
    config.load_kube_config(os.path.join(os.environ["HOME"], '.kube/config'))
except Exception as err:
    logging.error(f"The following error occured: {err}")

kube_cli = client.CoreV1Api()
lcd = i2c_lcd.lcd()


def get_nodes():
    nodes = kube_cli.list_node(watch=False)
    ready_nodes = 0
    total_nodes = len(nodes.items)

    for node in nodes.items:
        for condition in node.status.conditions:
            if condition.type == "Ready" and condition.status == "True":
                ready_nodes += 1

    return (ready_nodes, total_nodes)

def get_all_pods():
    pods = kube_cli.list_pod_for_all_namespaces(timeout_seconds=10)
    total_pods = len(pods.items)
    return total_pods

def print_welcome():
    date = datetime.date.today()
    time = datetime.datetime.now().strftime('%H:%M')

    lcd.lcd_clear()
    lcd.lcd_display_string('k3s lcd status svc', 1)
    lcd.lcd_display_string('running ^_^', 2)
    lcd.lcd_display_string(str(date), 3)
    lcd.lcd_display_string(str(time), 4)

def print_k3s_overview():
    ready_nodes, total_nodes = get_nodes()
    total_pods = get_all_pods()
    nodes_line = f"nodes ready: {ready_nodes}/{total_nodes}"
    pods_line = f"pods running: {total_pods}"

    lcd.lcd_clear()
    lcd.lcd_display_string('k3s status', 1)
    lcd.lcd_display_string(nodes_line, 2)
    lcd.lcd_display_string(pods_line, 3)

def run():
    logging.info("starting service")
    try:
        print("printing welcome message")
        print_welcome()
        time.sleep(DISPLAY_DELAY)

        while True:
            logging.info("printing k3s overview")
            print_k3s_overview()
            time.sleep(DISPLAY_DELAY)

            logging.info("printing welcome message")
            print_welcome()
            time.sleep(DISPLAY_DELAY)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run()
