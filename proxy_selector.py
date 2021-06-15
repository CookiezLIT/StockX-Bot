import random

proxy_path = 'proxies.txt'

def choose_proxy(proxy_path):
    '''
    reads the proxy.txt file and randomly selects a proxy
    :param proxy_path:path to the proxy file
    :return: a valid proxy, randomly chosen
    '''
    f = open('proxies.txt','r')
    proxies = f.read()
    proxies = proxies.split('\n')
    n = len(proxies)
    number = random.randint(0,n-1)

    proxy = proxies[number]
    if proxy == "":
        return ""
    details = proxy.split(':')
    ip = details[0]
    port = details[1]
    username = details[2]
    password = details[3]

    final_proxy = 'http://' + username + ':' + password + '@' + ip + ':' + port
    return final_proxy