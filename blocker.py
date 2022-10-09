from datetime import datetime
from xmlrpc.client import boolean
from colors import Colors as colors
import signal
import os
import sys
import getopt
import socket
from requests import get
import platform
import subprocess


def logo():
    os.system("clear")
    print(colors.R + colors.BOLD + """

     ▄▄▄▄    ██▓     ▒█████   ▄████▄   ██ ▄█▀▓█████  ██▀███
    ▓█████▄ ▓██▒    ▒██▒  ██▒▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
    ▒██▒ ▄██▒██░    ▒██░  ██▒▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
    ▒██░█▀  ▒██░    ▒██   ██░▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄
    ░▓█  ▀█▓░██████▒░ ████▓▒░▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
    ░▒▓███▀▒░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
    ▒░▒   ░ ░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
     ░    ░   ░ ░   ░ ░ ░ ▒  ░        ░ ░░ ░    ░     ░░   ░
     ░          ░  ░    ░ ░  ░ ░      ░  ░      ░  ░   ░
          ░                  ░

    """)


def usage():
    logo()
    print("""
    Blocker usage:

    -h    --help        print(this help and exit)
    -b    --block       Block Websites
    -u    --unblock     UnBlock Websites
    -r    --reset       Remove All Blocked Websites
    -d    --display     Display Host File
    -k    --Bkids       Block websites for kids
    -n    --Ukids       UnBlock websites for kids

    """)
    exit(1)


def signal_handler(signal, frame):
    logo()
    print(colors.O + "[" + colors.C + "*" + colors.O + "] " +
          colors.C + "Thank you" + colors.W)
    exit()


class blocker():
    def display(self):
        logo()
        self.check_root()
        self.userDetails()
        self.checkPath()

        if (self.isExist):
            self.displayHostFile()
        else:
            self.createHostFile()
            self.displayHostFile()

    def reset(self):
        logo()
        self.check_root()

        self.userDetails()
        self.checkPath()

        if (self.isExist):
            self.resetHostBlocker()
        else:
            self.createHostFile()
            self.resetHostBlocker()

    def blockKids(self):
        logo()
        self.check_root()
        self.userDetails()
        self.generateKidsList()
        self.checkPath()

        if (self.isExist):
            self.blockSites()
        else:
            self.createHostFile()
            self.blockSites()

    def unblockKids(self):
        logo()
        self.check_root()
        self.userDetails()
        self.generateKidsList()
        self.checkPath()

        if (self.isExist):
            self.unlbockSites()
        else:
            self.createHostFile()
            self.unlbockSites()

    def unblock(self):
        logo()
        self.check_root()
        self.userDetails()
        self.getWebsites(False)
        self.checkPath()

        if (self.isExist):
            self.unlbockSites()
        else:
            self.createHostFile()
            self.unlbockSites()

    def block(self):
        logo()
        self.check_root()

        self.userDetails()
        self.getWebsites(True)
        self.checkPath()

        if (self.isExist):
            self.blockSites()
        else:
            self.createHostFile()
            self.blockSites()

    def check_root(self):
        if os.geteuid() != 0:
            print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
                  "] " + colors.R + "You must be root; Say the magic word '" + colors.O + "sudo" + colors.R + "'" + colors.W)
            sys.exit(0)

    def generateKidsList(self):
        self.websites = ["yikyak.com", "reddit.com", "tiktok.com", "roblox.com", "whisper.sh",
                         "ask.fm", "4chan.org", "kik.com",
                         "Toomics.com", "Tumblr.com", "Chatroulette.com", "Archive.org",
                         "Twitter.com",
                         "theChive.com", "flickr.com",
                         "Monkey.cool", "Bovada.lv", "Toomics.com"]

        for i in range(len(self.websites)):
            print(self.websites[i])
            self.websites.append("http://" + self.websites[i])
            self.websites.append("https://" + self.websites[i])
            self.websites.append("http://www." + self.websites[i])
            self.websites.append("https://www." + self.websites[i])
            self.websites.append(self.websites[i])

    def getWebsites(self, isblock):
        print()
        try:
            if (isblock):
                inp = int(input(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
                                "] " + colors.W + "Please enter number of websites to block: "))
            else:
                inp = int(input(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
                                "] " + colors.W + "Please enter number of websites to unblock: "))
        except:
            print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
                  "] " + colors.R + "Please Enter only Digits" + colors.W)
            sys.exit(0)
        print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Please enter the websites " + colors.G + "[example.com]" + colors.W)
        print()
        for i in range(inp):
            website = input(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
                            "] " + colors.W)
            if not website.startswith("www.") and not website.startswith("https://"):
                self.websites.append("www." + website)
                self.websites.append("https://" + website)
                self.websites.append("https://www." + website)
                self.websites.append(website)
            elif website.startswith("https://") and not "www." in website:
                self.websites.append(website.replace(
                    "https://", "https://www."))
                self.websites.append(website.replace(
                    "https://", ""))
                self.websites.append(website)
            elif website.startswith("https://") and "www." in website:
                self.websites.append(website.replace("https://", ""))
                self.websites.append(website.replace("www.", ""))
                self.websites.append(website.replace("https://www.", ""))
                self.websites.append(website)

            if not website.startswith("http://") and not website.startswith("https://"):
                self.websites.append("http://" + website)
            elif website.startswith("www."):
                self.websites.append("http://" + website)

    def blockSites(self):
        print("\n" + colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Blocking Websites...")
        with open(self.host_path, 'r+') as hostsfile:
            hosts_content = hostsfile.read()
            for site in self.websites:
                if(site not in hosts_content):
                    hostsfile.write(self.IPAddr + " " + site + "\n")

        print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Websites have been blocked " + colors.G + self.checkmark + colors.W)

    def unlbockSites(self):
        print("\n" + colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "UnBlocking Websites...")
        with open(self.host_path, 'r+') as hostsfile:
            lines = hostsfile.readlines()
            hostsfile.seek(0)
            for line in lines:
                if not any(site in line for site in self.websites):
                    hostsfile.write(line)
            hostsfile.truncate()
        print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Websites have been unblocked " + colors.G + self.checkmark + colors.W)

    def resetHostBlocker(self):
        self.domainNames = ['.ae', '.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.arpa', '.academy', '.accountant', '.accountants', '.active', '.actor', '.ads', '.adult', '.aero', '.africa', '.agency',
                            '.airforce', '.amazon', '.analytics', '.apartments', '.app', '.apple', '.archi', '.army', '.art', '.arte', '.associates', '.attorney', '.auction', '.audible', '.audio', '.author', '.auto', '.autos', '.aws', '.sh', '.fm', '.cool', '.lv']
        print("\n" + colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "UnBlocking Websites...")
        with open(self.host_path, 'r+') as hostsfile:
            lines = hostsfile.readlines()
            hostsfile.seek(0)
            for line in lines:
                if not any(site in line for site in self.domainNames):
                    hostsfile.write(line)
            hostsfile.truncate()
        print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Websites have been unblocked " + colors.G + self.checkmark + colors.W)

    def checkPath(self):
        if(self.systemName == "Windows"):
            self.host_path = r"C:\Windows\System32\drivers\etc\hosts"
            self.isExist = os.path.exists(self.host_path)
        else:
            self.host_path = "/etc/hosts"
            self.isExist = os.path.exists(self.host_path)

    def displayHostFile(self):
        print(colors.BOLD + colors.O +
              "___________________________________________________" + colors.W)
        print()
        file = open(self.host_path, 'r')
        Lines = file.readlines()
        for line in Lines:
            print("{}".format(line.strip()))
        print()
        print(colors.BOLD + colors.O +
              "___________________________________________________" + colors.W)

    def createHostFile(self):
        print("\n" + colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Creating Host File")
        with open(self.host_path, 'w') as fp:
            pass
        print(colors.BOLD + colors.O + "[" + colors.R + "*" + colors.O +
              "] " + colors.W + "Host File has been created" + colors.G + self.checkmark + colors.W)

    def userDetails(self):
        self.hostname = socket.gethostname()
        self.IPAddr = socket.gethostbyname(self.hostname)
        self.systemName = platform.uname().system
        self.host_path = ""
        self.ip = ""
        self.localhost = "127.0.0.1"
        self.isExist = False
        self.websites = []
        self.checkmark = u'\u2713'

        print("{:<30} {:<40}".format(colors.W + "System Name", self.systemName))
        print("{:<30} {:<40}".format(colors.W + "Computer Name", self.hostname))
        print("{:<30} {:<40}".format(
            colors.W + "Local IP Address", self.IPAddr))
        try:
            self.ip = get('https://api.ipify.org').text
            print("{:<30} {:<30}".format(
                colors.W + "Public IP Address", self.ip))
        except:
            return
        print()


def main():
    if len(sys.argv) <= 1:
        usage()

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'buknrdh', [
            'block', 'unblock', 'Bkids', 'Ukids', 'reset', 'display', 'help'])
    except (getopt.GetoptError):
        print("1")
    for (o, a) in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-b', '--block'):
            b = blocker()
            b.block()
        elif o in ('-u', '--unblock'):
            b = blocker()
            b.unblock()
        elif o in ('-k', '--Bkids'):
            b = blocker()
            b.blockKids()
        elif o in ('-n', '--Ukids'):
            b = blocker()
            b.unblockKids()
        elif o in ('-r', '--reset'):
            b = blocker()
            b.reset()
        elif o in ('-d', '--display'):
            b = blocker()
            b.display()
        else:
            usage()


if __name__ == __name__:
    main()
