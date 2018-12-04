import ping
import socket
import time

def main():
    ttl = 1
    tries = 3
    arrived = False
    ipfound = False

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # take Input
    addr = input("Enter Domain Name : ") or "www.sustc.edu.cn"
    print('traceroute {0} ({1})'.format(addr, socket.gethostbyname(addr)))
    print("No. Address         rtts")


    while not arrived:
        s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        for i in range(0, tries):
            # Request sent
            ID = ping.single_ping_request(s, addr)

            rtt, reply, icmp_reply = ping.catch_ping_reply(s, ID, time.time())
            #print(rtt)

            if reply:
                reply['length'] = reply['Total Length'] - 20  # sub header

            if i == 0:
                print(str(ttl) , end=" ")

            if reply == None:
                print('*    ', end=" ")
                continue

            if socket.gethostbyname(addr) == reply["Source Address"]:
                #print("arrived")
                arrived = True

            if i == 0 or ipfound == False:
                print(str(reply["Source Address"]), end="   ")
                ipfound = True

            print(('{0:.2f} ms    '.format(rtt*1000)), end=" ")

        print("")
        ttl += 1
        ipfound = False

    # close socket
    s.close()
    return


if __name__ == '__main__':
    main()
