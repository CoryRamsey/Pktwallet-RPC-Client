import requests
import json
from requests.structures import CaseInsensitiveDict
from requests.auth import HTTPBasicAuth

# Launch pktwallet with './bin/pktwallet --rpclisten 127.0.0.1:8332 -u pkt -P tkp --noservertls'

#Wallet address to pay from (must already be created and managed by pktwallet daemon)
house_wallet = ""

#pktwallet server address and credentials
pktw_url = "http://127.0.0.1:8332/"
pktw_user = "pkt"
pktw_pass = "tkp"


#RPC call function
def make_call(command, params):
        #format headers
        headers = CaseInsensitiveDict()
        headers["content-type"] = "text/plain;"
        
        #assemble json data
        data = '{"jsonrpc":"1.0","method":"' + command + '","params":[' + params + '],"id":1}'
        
        ### debug
        print ("Data:" + data)

        #Perform and display the request/response
        req = requests.post(pktw_url, headers=headers, data = data, auth = HTTPBasicAuth(pktw_user, pktw_pass))
        print(req.json())
        del req, data

#send pkt from house wallet
#if sending less than 1 pkt, lead with 0 (e.g. 0.185) TODO
def send_pkt(address, amount):
    p = '"' + address + '",' + amount + ',["' + house_wallet + '"]'
    print (f"the send pkt call: {p}")
    make_call("sendfrom", p)
    del p

#Unlock Wallet
def unlock_wallet():
    seconds = input("How many seconds? ")
    if seconds == "0":
        make_call("walletpassphrase", '"none", ' + seconds)
        print("Attempted to unlock the wallet indefinitely")
        del seconds
    else:
        make_call("walletpassphrase", '"none", ' + seconds)
        print(f"Attempted to unlock the wallet for {seconds} seconds")
        del seconds

#Get entire wallet balance
def get_balance():
    make_call("getbalance", "")

#Get wallet info
def get_info():
    make_call("getinfo","")

#Get list of received pkt
def list_received():
    make_call("listreceivedbyaddress", "")


#main program loop until SIGINT
while (True):
    request = input("Enter Command: ")
    if request == "unlock":
        unlock_wallet()        
    elif request == "balance":
        get_balance()
    elif request == "info":
        get_info()
    elif request == "listreceived":
        list_received()
    elif request == "send":
        to_addr = input("Enter receiver address: ")
        send_amt = input("Enter amount to send: ")
        send_pkt(to_addr, send_amt)
        print (f"Attempted to send {send_amt} pkt")
        del to_addr
        del send_amt





