import pandas as pd
import time
import requests
btc = '3QzYvaRFY6bakFBW4YBRrzmwzTnfZcaA6E' # Genesis Block
print("source wallet is: ",btc)
#btc = '3QHUqRPGn28MkcgtNakseEygJjTchVQjDF'
def count_tran(btc):
        transactions_url = 'https://blockchain.info/rawaddr/' + btc
        df = pandas.read_json(transactions_url)
        count = df['n_tx']
        print("All count of transactions",count[0])
        return count
#def bash_get_file(btc,count):
#        os.system('wget https://blockchain.info/rawaddr/$btc')

#@dataclass
#class Returnvalue:
    #y0: list
    #y1: list
    #y3: list
def get_all_tran(btc,count):
        offeset=0
        format_money=100000000
        all_info=[]
        addr_sender=[]
        money_send=[]
        data_send=[]
        all_money=0
        str_info=[]
        
        df = pd.read_json('import.json')
        transactions = df['txs']
        for i in range (0,count):
                print("source addr:",
                        transactions[i]['inputs'][0]['prev_out']['addr'],
                        "send",(float(transactions[i]['out'][0]['value'])/format_money),
                        "time of trsansaction", time.strftime("%D %H:%M", time.localtime(int(transactions[i]['time']))))
                addr_sender.append(transactions[i]['inputs'][0]['prev_out']['addr'])
                money_send.append(float(transactions[i]['out'][0]['value'])/format_money)
                data_send.append(str(time.strftime("%D %H:%M", time.localtime(int(transactions[i]['time'])))))
                all_money+=(float(transactions[i]['out'][0]['value'])/format_money)
        print("all money is: ",all_money)
        #return ReturnValue(addr_sender,money_send,data_send)
        return str_info

#z=count_tran(btc)
x=get_all_tran(btc,5000)

list_uniq={i:x.count(i) for i in x}
print("folowers: ",list_uniq)
#['spending_outpoints'])
