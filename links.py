#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests, sys, os
import random, string
import urllib
import re

class Links:
    def download(self, theurl, thedir):
        print("[i] Downloading file to: "+thedir)
        urllib.urlretrieve(theurl, thedir)

    def get_ahref_link(self):
        for link in self.soup.find_all('a', href=True):
            if (link['href'][0:4]!='http'):
                self.links.add(self.host + link['href'])
            else:
                self.links.add(link['href'])

    def get_resource_link(self):
        print("TODO")
        for link in self.soup.find_all('video', src=True):
            if (link['src'][0:4]!='http'):
                self.links.add(self.host + link['src'])
            else:
                self.links.add(link['src'])

    def exec_regex(self,regex):
        context = "\n".join(self.links)
        results = set(re.compile(regex).findall(context))
        self.links = results

    def print_links(self,mode):
        if mode == True:
            print(" ".join(self.links))
        else:
            if self.type == 0:
                ltype = "All"
            elif self.type == 1:
                ltype = "Resource"
            else:
                ltype = "Visible"
            print("Reference\n\n  "+ltype+" Links:")
            i=0
            for link in self.links:
                i=i+1
                print("  "+str(i)+". "+link)

    def __init__(self, host, main=False, args={'r':False,'a':False,'d':False,'l':False,'e':None}):
        # Fixing the trailing / in host
        self.host = host if host[-1:]!='/' else host[:-1]

        # If there is a dot in the domain name
        if "." in self.host.split("/")[-1]:
            # Get the protocol
            self.proto = self.host.replace(self.host.split("/")[-1],"")

        # Make the request and download the page
        try:
            resp = requests.get(host)
            encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
            # Maybe it will be usefull in future
            self.page = resp.content
        except requests.exceptions.ConnectionError:
            exit("[!] Conneciton Error: are you sure the URL is correct?")
        self.soup = BeautifulSoup(self.page, "lxml", from_encoding=encoding)
        # Such a list
        self.links = set()

        if args['r'] == True:
            self.type = 1 # Resource (audio,video,img,background-img)
            self.get_resource_link()
        elif args['a'] == True:
            self.type = 0 # All (Visible + Resource)
            self.get_ahref_link()
            self.get_resource_link()
        else:
            self.type = 2 # Visible (a href)
            self.get_ahref_link()

        # RegEx P0w3r
        if args['e'] != None:
            self.exec_regex(args['e'])
        
        # Can we print?
        if main == True:
            self.print_links(args['l'])
            if args['l'] == False AND args['d'] == True:
                for link in self.links:
                    self.download(link,link.split("/")[-1])
            
        return self.links


# Usage as an object:
# from links import Links
# Links("http://thezero.org")
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='links')
    parser.add_argument('url', help='target web page')
    parser.add_argument('-l', action='store_true', help='output found links as plain list')
    parser.add_argument('-d', action='store_true', help='download resource directly in CWD')
    parser.add_argument('-a', action='store_true', help='select resource and visible links')
    parser.add_argument('-r', action='store_true', help='select only resource links (audio,video,img,background)')
    parser.add_argument('-e', help='select links that follow RegEx')

    args = vars(parser.parse_args())
    host = args['url']
    del args['url']

    Links(host,args=args,main=True)
