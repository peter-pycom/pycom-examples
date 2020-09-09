import time
import os
import binascii

u = None

pins = {
    'GPy' : ('P5', 'P98', 'P7', 'P99')
}

def init(br=None):
    global u
    if u:
        return True
    if br:
        print('init(', br, ')')
        u = UART(1, baudrate=br, pins=pins[os.uname().sysname], timeout_chars=10)
        try:
            at()
            print('init(', br, ') succeeded')
            return True
        except Exception as e:
            print('init(', br, ') failed', e)
            try:
                at()
                print('init(', br, ') succeeded')
                return True
            except:
                print('init(', br, ') failed', e)
                return False
    else:
        return init(921600) or init(115200)

def help(verbose=False):
    init()
    r = at('AT+CLAC', do_return=True)
    if verbose:
        for cmd in r:
            at(cmd + '=?')
    else:
        for cmd in r:
            print(cmd, end=' ')

def at(cmd='', pretty=True, verbose=False, do_return=False):
    init()
    if do_return:
        retval = []
    else:
        retval = False
    if not cmd:
        cmd='AT'
        verbose = True
    if verbose:
        print('[', cmd, ']', sep='', end=':')

    u.write((cmd + '\r\n').encode())
    time.sleep_ms(1000)
    r = u.read()
    # print("[", len(r), "]<", binascii.hexlify(r), ">", sep='', end='')
    try:
        for line in r.decode().split('\r\n'):
            if len(line) == 0:
                continue
            else:
                if do_return:
                    retval += [line]
                    if verbose:
                        print(line)
                else:
                    if line == 'OK':
                        retval = True
                        if verbose:
                            print(line)
                    elif line == 'ERROR':
                        retval = False
                        if verbose:
                            print(line)
                    else:
                        print(line)
        return retval
    except:
        print("[", len(r), "]<", binascii.hexlify(r), ">", sep='', end='')
        print()

def smod():
    init()
    r = at('AT+SMOD?', do_return=True)
    print(r, end=' ')
    m = int(r[0])
    if m == 0:
        print('FFH (bootloader)')
    elif m == 1:
        print('mTools')
    elif m == 2:
        print('FFF (application)')
    elif m == 3:
        print('dunno')
    elif m == 4:
        print('upgrade???')
    else:
        print('?')



if __name__ == '__main__':
    # init(921600) or init(115200)
    # at('AT', verbose=True)
    # at('AT+SMOD?')
    # at('AT+BMOD?')
    # smod()
    at('AT+SMSWBOOT=?')
    # help(True)
