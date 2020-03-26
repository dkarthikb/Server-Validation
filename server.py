import sys
import json
import paramiko
import getpass
import logging
import re
logging.basicConfig(level=logging.INFO, filename='sample.log', format='%(asctime)s :: %(levelname)s :: %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s ')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

'''Loading command'''
def loadJSON(filename):
    with open(filename,"r") as f:
        data= json.load(f)
    return data
def sshConnect(host,username,password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try :
        client.connect(host, username=username, password=password)
    except paramiko.ssh_exception.AuthenticationException:
        logging.error("Invalid USERNAME or PASSWORD")
        sys.exit(1)

    return client

def ritmType(ritm):
    if re.search(r'tc',ritm,re.IGNORECASE):
        logging.info("RITM Type :")
    elif re.search(r'batch',ritm,re.IGNORECASE):
        logging.info("RITM Type :")
    else:
        logging.error("Invalid RITM TYPE")
        sys.exit(1)

if __name__ == '__main__':
    username = input("Enter Username:")
    password = getpass.getpass("Enter Password:")
    setupJSON = loadJSON("setup.json")
    commandJson = loadJSON("command.json")

    for key, value in setupJSON['envClassifierToAdd'].items():
        for hostName in value.split(","):
            sshClient = sshConnect(hostName,username,password)
            logging.info("Hostname :" + hostName.ljust(25))
            for cKey , cValue in commandJson.items():
                if cKey == "mountPoint":
                    for mKey, mValue in cValue.items():
                        stdin, stdout, stderr = sshClient.exec_command(mValue)
                        if stderr.read().decode():
                            logging.warning(mKey + " : " + mValue+ "Mount unavailable ".ljust(25).rstrip())
                        else:
                            logging.info(mKey + " : " +  stdout.read().decode().ljust(25).rstrip())
                else:
                        stdin, stdout, stderr  = sshClient.exec_command(cValue)
                        logging.info(cKey + " : " +  stdout.read().decode().ljust(25).rstrip())
