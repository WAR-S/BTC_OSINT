import urllib

import pandas as pd
import time
import networkx as nx

btc = '3QzYvaRFY6bakFBW4YBRrzmwzTnfZcaA6E'  # Genesis Block
print("source wallet is: ", btc)
format_money = 100000000


def count_tran(btc):
    transactions_url = 'https://blockchain.info/rawaddr/' + btc
    df = pd.read_json(transactions_url)
    count = df[ 'n_tx' ]
    print("All count of transactions", count[ 0 ])
    urllib.request.urlretrieve(transactions_url+"?offset="+count[0], "mp3.mp3")
    return count


# def bash_get_file(btc,count):
#        os.system('wget https://blockchain.info/rawaddr/$btc')
list_m = [ ]


def uniq_normalize(lst1, lst2):
    sum_per_node = 0
    total = 0
    sum_per_node_lst = [ ]
    ret_lst1 = [ ]
    ret_lst2 = [ ]
    for i in range(0, len(lst1)):
        for j in range(1, len(lst1)):
            if lst1[ i ] == lst1[ j ]:
               # print("found dubl icate",lst1[i])
                sum_per_node += lst2[ j ]
                total += lst2[ j ]
                #print(sum_per_node)
        ret_lst1.append(lst1[ i ])
        sum_per_node_lst.append(sum_per_node)
        sum_per_node = 0
    dictionary1 = dict(zip(ret_lst1, sum_per_node_lst))
    #print(dictionary1)
    #print("total money ", total)
    #print("total uniq tranzaction ", len(ret_lst1))
    list_m = sum_per_node_lst
    return dictionary1


def get_all_tran(btc, count):
    addr_sender = [ ]
    money_send = [ ]
    dst_addr = [ ]
    data_send = [ ]
    all_money = 0
    dst_self_money = [ ]
    all_self_send = 0
    dst_self_addr = [ ]
    dst_seld_date = [ ]
    scatic_mass = [ ]
    btc_c_self = 0
    btc_c_dest = 0
    df = pd.read_json('./import_full.json')
    transactions = df[ 'txs' ]
    for i in range(0, count-1):
        if (str(transactions[ i ][ 'inputs' ][ 0 ][ 'prev_out' ][ 'addr' ]) == btc):
            # "internal transaction"
            btc_c_self += 1
            scatic_mass.append(transactions[ i ][ 'inputs' ][ 0 ][ 'prev_out' ][ 'addr' ])
            log_z = transactions[ i ][ 'inputs' ][ 0 ][ 'prev_out' ][ 'addr' ]
            dst_self_money.append(float(transactions[ i ][ 'out' ][ 0 ][ 'value' ]) / format_money)
            dst_self_addr.append(transactions[ i ][ 'out' ][ 0 ][ 'addr' ])
            dst_seld_date.append(str(time.strftime("%D %H:%M", time.localtime(int(transactions[ i ][ 'time' ])))))
            all_self_send += (float(transactions[ i ][ 'out' ][ 0 ][ 'value' ]) / format_money)
        else:
            # /"external transaction"
            btc_c_dest += 1
            addr_sender.append(transactions[ i ][ 'inputs' ][ 0 ][ 'prev_out' ][ 'addr' ])
            dst_addr.append(transactions[ i ][ 'out' ][ 0 ][ 'addr' ])
            money_send.append(abs((transactions[ i ]['result']) / format_money))
            data_send.append(str(time.strftime("%D %H:%M", time.localtime(int(transactions[ i ][ 'time' ])))))
            all_money +=((transactions[ i ]['result']) / format_money)

    #print(len(scatic_mass))
    #print(len(dst_self_addr))
    #print(dst_self_money)
    #external
    z = uniq_normalize(addr_sender, money_send)
    #internal
    #z = uniq_normalize(dst_self_addr, money_send)
    #print("all money get: ", all_money, "count tranzaction", btc_c_self)
    #print("all money sent: ", all_self_send, "count transaction", btc_c_dest)
    # internal
    #print(len(z))
    #print(len(dst_self_addr))
    #print(len(dst_self_money))

    #graf_internal(z,dst_self_money,dst_self_addr)
    # external
    graf_internal(z, money_send, dst_addr)
    print(all_money)

    return addr_sender


def gen_edge_with_weight(graph, dst_self_money):
    return dict(zip(graph, dst_self_money))


def generate_edges(graph):
    edges = [ ]
    for node in graph:
        edges.append((node, btc))
    print(edges)
    return edges


def gen_tulple(graph, dst_self_money):
    t = ()
    temp = [ ]
    print (len(graph.keys()))
    print (btc)
    print(len(dst_self_money))
    for i in range(0, len(graph)):
        t = list(graph.keys())[ i ], btc, dst_self_money[ i ]
        temp.append(t)
    print(temp)
    return temp


def graf_internal(dictionary1, dst_self_money, dst_addr):
    G = nx.Graph()
    edges = (generate_edges(dictionary1))
    q = gen_tulple(dictionary1, dst_self_money)
    print(q)
    G.add_weighted_edges_from(q)
    print('узлы', len(G.nodes))
    print('рёбра', len(G.edges))
    nx.write_gexf(G, "./test.gexf")
    return

if __name__ == '__main__':
    get_all_tran(btc, 5000)
