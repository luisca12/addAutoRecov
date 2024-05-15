from netmiko import ConnectHandler
from functions import *
from log import *
from strings import *
from auth import *

import os
import traceback
import re

shAutoRecov = "show run | include errdisable"
shHostname = "show run | i hostname"

addAutoRecov = [
        "errdisable recovery cause dhcp-rate-limit",
        "errdisable recovery interval 600",
        "do wr"
]

def addRecov(validIPs, username, netDevice):
    # This function is to add Auto Recovery
    
    for validDeviceIP in validIPs:
        try:
            validDeviceIP = validDeviceIP.strip()
            currentNetDevice = {
                'device_type': 'cisco_xe',
                'ip': validDeviceIP,
                'username': username,
                'password': netDevice['password'],
                'secret': netDevice['secret'],
                'global_delay_factor': 2.0,
                'timeout': 120,
                'session_log': 'netmikoLog.txt',
                'verbose': True,
                'session_log_file_mode': 'append'
            }

            print(f"INFO: Connecting to device {validDeviceIP}...")
            with ConnectHandler(**currentNetDevice) as sshAccess:
                authLog.info(f"User {username} is now running commands at: {validDeviceIP}")
                sshAccess.enable()
                shHostnameOut = sshAccess.send_command(shHostname)
                authLog.info(f"User {username} successfully found the hostname {shHostnameOut}")
                shHostnameOut = shHostnameOut.replace('hostname', '')
                shHostnameOut = shHostnameOut.strip()
                shHostnameOut = shHostnameOut + "#"

                print(f"INFO: Configuring the following commands in {validDeviceIP}: \n{addAutoRecov[0]}\n{addAutoRecov[1]}")
                authLog.info(f"Configuring the following commands in {validDeviceIP}: \n{addAutoRecov[0]}\n{addAutoRecov[1]}")
                sshAccess.send_config_set(addAutoRecov)
                print(f"INFO: Successfully configured auto recovery for device: {validDeviceIP}")
                authLog.info(f"Successfully configured auto recovery for device: {validDeviceIP}")

                with open(f"{validDeviceIP}_Outputs.txt", "a") as file:
                    file.write(f"User {username} connected to device IP {validDeviceIP}\n\n")
                    print(f"INFO: Validating the configuration done...\n{shHostnameOut}{shAutoRecov}")
                    shAutoRecovOut = sshAccess.send_command(shAutoRecov)
                    print(f"{shAutoRecovOut}")
                    authLog.info(f"Automation successfully ran the command: {shAutoRecov}")
                    file.write(f"{shHostnameOut}{shAutoRecov}:\n{shAutoRecovOut}")

        except Exception as error:
            print(f"An error occurred: {error}\n", traceback.format_exc())
            authLog.error(f"User {username} connected to {validDeviceIP} got an error: {error}")
            authLog.debug(traceback.format_exc(),"\n")
            with open(f"failedDevices.txt","a") as failedDevices:
                failedDevices.write(f"User {username} connected to {validDeviceIP} got an error: {error} \n")
        
        finally:
            with open(f"generalOutputs.txt", "a") as file:
                    file.write(f"INFO: Taking a \"{shAutoRecov}\" for device: {validDeviceIP}\n")
                    file.write(f"{shHostnameOut}{shAutoRecov}:\n{shAutoRecovOut}\n")
            print("\nOutputs and files successfully created.")
            print("For any erros or logs please check authLog.txt\n")