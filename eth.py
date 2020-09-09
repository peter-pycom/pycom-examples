from network import ETH
import time
import os
import machine
import binascii

e = None

def init():
    global e
    if e is None:
        name = os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:]
        e = ETH(hostname=name) # binascii.hexlify(machine.unique_id()))
        print(name, "eth.py")
        print("eth mac", binascii.hexlify(e.mac()))
    return

def reconnect(ip_mask_gw_dns=None):
    init()
    if e.isconnected():
        print("already connected, deinit first")
        e.deinit()
        while e.isconnected():
            # wait for connection to go down
            pass
            # print(eth.isconnected())
        print("eth re-init")
        e.init()
    return connect(ip_mask_gw_dns)

def connect(config=None):
    init()
    if e.isconnected():
        print('already connected')
        return True
    # (ip, subnet_mask, gateway, DNS_server)
    # eth.ifconfig(config=('192.168.0.107', '255.255.255.0', '192.168.0.1', '192.168.0.1')) # use this!
    # eth.ifconfig(config=('192.168.0.107', '255.255.255.0', '192.168.0.1', '8.8.8.8')) # doesn't work?
    #### eth.ifconfig(config=('10.107.107.107', '255.0.0.0', '10.0.103.1', '10.0.103.1'))
    if config:
        if config.__class__.__name__ == 'tuple':
            pass
        else:
            if config == '192.168.0.107' or config == 107:
                print('guessing config for', config)
                config = ('192.168.0.107', '255.255.255.0', '192.168.0.1', '192.168.0.1')
        print("using fixed ip config:", config)
        e.ifconfig(config=config)
    print("connecting eth ...")
    i = 0
    for i in range(0,50):
        if e.isconnected():
            print("... eth connected")
            break
        else:
            print(i, "waiting for connection", e.ifconfig()) #, end=" ")
            time.sleep(0.5)
        i+=1

    if e.isconnected():
        print("hostname", e.hostname())
        print("isconnected", e.isconnected())
        print("ifconfig", e.ifconfig()) # (ip, subnet_mask, gateway, DNS_server)
        return True
    else:
        print("FAILED to connect eth")
        return False

def ifconfig():
    init()
    print("ifconfig", e.ifconfig()) # (ip, subnet_mask, gateway, DNS_server)

def disconnect():
    if e:
        e.deinit()

if __name__ == "__main__":
    config = None
    # config=('192.168.0.1', '255.255.255.0', '192.168.0.1', '192.168.0.1')
    # config = ('192.168.0.107', '255.255.255.0', '192.168.0.1', '192.168.0.1')
    # connect(config)
    reconnect(107)
    # connect()
