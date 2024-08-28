import requests
import csv
from stem import Signal
from stem.control import Controller
import re
import time
from random import choice

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


# r = requests.get('https://edmundmartin.com', headers=random_headers())

outputFile = open("outputFile.csv", 'a+')
fileField = ['Emails', 'Status']
writer = csv.DictWriter(outputFile, fieldnames=fileField)
writer.writeheader()

def main():
    readcsv = csv.reader(open("input.csv", 'r'), dialect='excel')

    for index, email in enumerate(readcsv):
        outputFile = open("outputFile.csv", 'a+', newline='')
        writer = csv.DictWriter(outputFile, fieldnames=fileField)
        # time.sleep(5)
        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9150'
        session.proxies['https'] = 'socks5h://localhost:9150'
        head = session.headers.update(random_headers())
        print(session.headers)
        ip = session.get('https://api.ipify.org', headers=head).text
        print('My public IP address is: {}'.format(ip))
        source = session.get('https://verify-email.org/home/verify-as-guest/'+str(email), headers=head)
        content = source.content
        print(content)

        if '"status":1' in str(content):
            content = 'OK'
            print(content)
            writer.writerow({'Emails': email, 'Status': str(content)})
        elif '"status":0' in str(content):
            content = 'No'
            print(content)
            writer.writerow({'Emails': str(email), 'Status': str(content)})
        elif '"status":-1' in str(content):
            content = 'Unknown'
            print(content)
            writer.writerow({'Emails': str(email), 'Status': str(content)})
        elif "You have reached the limit of 5 emails per hour" in str(content):
            with Controller.from_port(port=9151) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
            index -= 1

        with Controller.from_port(port=9151) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)



        outputFile.close()



if __name__ == '__main__':
    init = time.time()
    main()
    total = time.time() - init
    h = total / 3600
    dh = total % 3600
    m = dh / 60
    s = dh % 60
    D = total / 86400

    print('time is = (%d) Day ----- %dh : %dm : %ds ' % (D, h, m, s))