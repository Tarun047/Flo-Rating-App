import subprocess
from more_itertools import sliced
import json


def writeUnitToBlockchain(text,receiver,amt):
    txid = subprocess.check_output(["flo-cli","--testnet", "sendtoaddress",receiver,str(amt),'""','""',"true","false","10",'UNSET',str(text)])
    txid = str(txid)
    txid = txid[2:-3]
    return txid

def writeDatatoBlockchain(text,receiver,amt):
    n_splits = len(text)//350 + 1                                                               #number of splits to be created
    splits = list(sliced(text, 350))                                                            #create a sliced list of strings
    tail = writeUnitToBlockchain(splits[n_splits-1],receiver,amt)       #create a transaction which will act as a tail for the data
    cursor = tail
    if n_splits == 1:
        return cursor                                                                           #if only single transaction was created then tail is the cursor

    #for each string in the list create a transaction with txid of previous string
    for i in range(n_splits-2,-1,-1):
        splits[i] = 'next:'+cursor+" "+splits[i]
        cursor = writeUnitToBlockchain(splits[i],receiver,amt)
    return cursor

def readUnitFromBlockchain(txid):
    rawtx = subprocess.check_output(["flo-cli","--testnet", "getrawtransaction", str(txid)])
    rawtx = str(rawtx)
    rawtx = rawtx[2:-3]
    tx = subprocess.check_output(["flo-cli","--testnet", "decoderawtransaction", str(rawtx)])
    content = json.loads(tx)
    text = content['floData']
    return text

def readDatafromBlockchain(cursor):
    text = []
    cursor_data = readUnitFromBlockchain(cursor)
    while(cursor_data[:5]=='next:'):
        cursor = cursor_data[5:69]
        #print("fetching this transaction->>"+cursor)
        text.append(cursor_data[70:])
        cursor_data = readUnitFromBlockchain(cursor)
    text.append(cursor_data)
    #print(text)
    text=('').join(text)
    return text
