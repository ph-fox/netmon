import os, time
import threading
from concurrent.futures import ThreadPoolExecutor
from getmac import get_mac_address
from mac_vendor_lookup import MacLookup
from icmplib import ping
from colorama import Fore

live = []
ipz = '192.168.1.'

def check2(ip):
    print("Scanning "+ip)
    host = ping(ip, count=5, interval=.1, timeout=2, privileged=True)
    if host.is_alive:
#        live.append(ip)
        f=open('save_host.txt','a')
        f.write(ip+'\n')
        f.close()
    else:
        return False


def check(ip):
    host = ping(ip, count=1, interval=.1, timeout=1, privileged=True)
    if host.is_alive:
        return True
    else:
        return False

def mon():
    while True:
        live_hosts = []
        dead_hosts = []
        hosts_list = open('save_host.txt').read().splitlines()
        executor = ThreadPoolExecutor(max_workers=3)
        for host in hosts_list:
            #mac = get_mac_address(host)
            #vend = MacLookup().lookup(mac)
            checker = executor.submit(check, host)
            isLive = checker.result()
            if isLive:
                live_hosts.append(f"{host}")
            else:
                dead_hosts.append(f"{host}")

        os.system('cls')
        print(Fore.BLUE+"="*40)
        print(f"|{Fore.YELLOW}Status{Fore.BLUE}|{Fore.YELLOW} Ip Address{Fore.BLUE} |{Fore.YELLOW} Mac{Fore.BLUE} |{Fore.YELLOW} Vendor{Fore.BLUE}")
        print("="*40)
        for lh in live_hosts:
            print(f"{Fore.BLUE}|[{Fore.GREEN}LIVE{Fore.BLUE}] {Fore.YELLOW}{lh}")
        for dh in dead_hosts:
            print(f"{Fore.BLUE}|[{Fore.RED}DEAD{Fore.BLUE}] {Fore.YELLOW}{dh}")
        print(Fore.BLUE+"="*40)
        print("|  BY: Anikin Luke Abales <|> Ph-Fox ")        
        print(Fore.BLUE+"="*40)

def ss():
    print("Running save scan!")
    for ip in range(100):
        host_ip = ipz+str(ip)
        threading.Thread(target=check2, args=[host_ip]).start()
    print('Done!')
    print('waiting 20secs')
    time.sleep(2)
    for host in live:
        f=open('save_host.txt','a')
        f.write(host+'\n')
        print(host)
    mon()

if __name__ == "__main__":
    if(os.path.exists('save_host.txt')is False):
        ss()
    else:
        print('Host list found from the last scan!')
        ui = input('Do you want to scan again?(y/N): ').lower()
        if ui == 'y':
            os.system('del save_host.txt')
            ss()
        else:
            print('Starting to monitor..')
            mon()


"""
192.168.1.1
192.168.1.2
192.168.1.7
192.168.1.9
192.168.1.13
192.168.1.19
"""
