#!/usr/bin/env python
"""Manages an ssh reverse tunnel. 
see http://en.gentoo-wiki.com/wiki/Reverse_Tunneling
The tunnel is switched on and off through a google doc, which is checked every
few minutes.
autossh is used to set up the tunnel. ssh should be configured correctly (with
keys and such) to make it work.
you will need gdata of at least 2.0.17, I think.
config options go into settings.py; you will need to make your own.
below is what needs to go in it.

USER = "<someone>@gmail.com"
PASSWORD = "<your password>"
FOLDER = "<some folder>"
DOC = "<some document in that folder>"
TARGET_HOST = "<remote host>"
REMOTE_PORT = <port on remote host>
LOCAL_PORT = <port to send to on local host>
TIME_SECONDS = 60 * 5 # i.e. 5 minutes

once you've got it set up, let it run.
"""

import gdata.docs.service
import tempfile
import functools
import re
import os, signal, subprocess
import time
from settings import *

RE_TRUE = re.compile("true|yes|on|1", re.I)

def download_and_load(client, entry):
    """downloads the gdoc entry as a text file to a temp file and reads the
    contents."""
    tmp = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    client.Export(entry, tmp.name)
    return tmp.read()

def get_tunnel_state_req():
    """gets the tunnel var state by examining the doc specified above"""
    client = gdata.docs.service.DocsService()
    client.ClientLogin(USER, PASSWORD)
    dl_ld = functools.partial(download_and_load, client)
    query = gdata.docs.service.DocumentQuery()
    query.AddNamedFolder(USER, FOLDER)
    feed = client.QueryDocumentListFeed(query.ToUri())
    entries = [e for e in feed.entry if e.title.text == DOC]
    return False if (not entries) else bool(RE_TRUE.search(dl_ld(entries[0])))

def autossh():
    """Runs autossh to implement the tunnel"""
    cmd = ["autossh",
           "-M", "0",
           "-q",
           #"-f",
           "-N",
           "-o", "ServerAliveInterval 60",
           "-o", "ServerAliveCountMax 3",
           "-R" 
           "%d:localhost:%d" % (REMOTE_PORT, LOCAL_PORT),
           TARGET_HOST]
    return subprocess.Popen(cmd)


def main():
    """main function."""
    os.environ['AUTOSSH_GATETIME'] = '0'
    conn = None
    while True:
        print("checking... ")
        req = False
        try:
            req = get_tunnel_state_req()
            print("checked.")
        except:
            print("failed, skipping.")
        #only 2 things action is needed on -
        #tunnel is inactive and is req'd on
        if (not conn) and req:
            print("starting connection... ")
            conn = autossh()
            print("connected.")
        #tunnel is active and req'd off
        elif conn and (not req):
            print("stopping connection... ")
            os.kill(conn.pid, signal.SIGTERM)
            conn = None
            print("stopped.")
        #wait.
        time.sleep(TIME_SECONDS)

if __name__ == '__main__':
    main()
