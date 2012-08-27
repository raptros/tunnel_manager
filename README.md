# Tunnel Manager!
A python script to manage a reverse SSH tunnel by checking a google document.

## What? Why?
SSH reverse tunneling creates a way to connect back to the host that initiated
the connection. See [revtun] [] for more. This script allows a tunnel to be
controlled by the contents of a google document. Why? Because I'd rather not
keep an ssh tunnel to ... semi-public machines open all the time.

## Setup
You'll need
* python with the [gdata] [] module installed. Preferably 2.0.17 (or higher).
* [autossh] []; this keeps the ssh client running.
* see [revtun] [] to make sure you know what's going on and what needs to be
  the case for reverse tunneling to work.

Once you've got these set up, you'll need to create a setup.py. Here's an example:
```python 
USER = "<someone>@gmail.com"
PASSWORD = "<your password>"
FOLDER = "<some folder>"
DOC = "<some document in that folder>"
TARGET_HOST = "<remote host>"
REMOTE_PORT = <port on remote host>
LOCAL_PORT = <port to send to on local host>
TIME_SECONDS = 60 * 5 # i.e. 5 minutes
```

## Usage
In google docs, create a document (in a folder); both should have easy names.
Do the setup to point at this file. Run tunnel_manager.py.
* To start the tunnel - put `yes`, `true`, `1`, `on`, or some variation of those in the
  file, and wait - at the next check, the tunnel will be created.
* To stop the tunnel - basically clear the file. As long as it doesn't contain
  anything like the activating strings, on the next check the script will kill
  the tunnel.

[revtun]: http://en.gentoo-wiki.com/wiki/Reverse_Tunneling (Reverse Tunneling)
[autossh]: http://www.harding.motd.ca/autossh/ (Autossh)
[gdata]: https://code.google.com/p/gdata-python-client/ (gdata-python-client)
