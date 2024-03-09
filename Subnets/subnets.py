import tkinter as tk
import ipaddress
import math
from tkinter import ttk
from tkinter.messagebox import showinfo

def test_data(ip,nets,hosts):
    ip.set("8.8.8.0/24")
    nets.set("10")
    hosts.set("7")

def split_input(ip_text):
    ip_and_mask = ip_text.split('/')
    try:
        ip_addr = ipaddress.IPv4Address(ip_and_mask[0])
    except ValueError:
        raise ValueError("ValueError for IP Address Format") 
    result = [int(ip_addr)]
    result.append(int(ip_and_mask[1]))
    return result

def int_to_ip(value):
    try:
        ip_addr = ipaddress.IPv4Address(value)
        return str(ip_addr)
    except ValueError:
        lbl_result["text"] = "ValueError for IP Address Format"

def ip_to_int(ip_str):
    try:
        ip_addr = ipaddress.IPv4Address(ip_str)
        result = int(ip_addr)
        return result
    except ValueError:
        lbl_result["text"] = "ValueError for IP Address Format"

def net_ips(masked_bits):
    host_bits = 32 - masked_bits
    available_ips = (2 ** host_bits) - 2    # account for net and broadcast
    return available_ips

def mask_ips(masked_bits):  # return nr of ips in mask
    result = ((2 ** masked_bits))
    return result

def host_bits(nr_of_addresses): # return host bits for nr of addresses
    total_addr = nr_of_addresses
    result = math.ceil(math.log2(total_addr))
    return result

# validations
def is_ip_ok(str):
    try:
        ipaddress.ip_address(str)
        return True
    except ValueError:
        return False
    
def is_mask_ok(str):
    if (int(str) >= 0) and (int(str) < 32):
        return True
    else:
        return False

def is_input_ok(list):
    if is_ip_ok(list[0]) and is_mask_ok(list[1]):
        return True
    else:
        return False

def subnets_calc():
    try:
        parsed = split_input(ip.get())
    except:
        lbl_result["text"] = "ValueError for IP Address Format"
        return
    
    if not is_input_ok(parsed):
        lbl_text = "Please input a correct IP address and mask"
        lbl_result["text"] = lbl_text
        return

    txt_box.delete("1.0", "end")
    
    nets = int(nets_entry.get())
    hosts = int(hosts_entry.get())+2
    first_net = split_input(ip.get())[0]
    mask = split_input(ip.get())[1]

    needed_mask = host_bits(hosts+2)
    needed_ips = nets * mask_ips(needed_mask)
    total_ips = net_ips(mask)
    if (needed_ips > total_ips):
        lbl_text = "Not Possible"
        lbl_result["text"] = lbl_text
        return

    #Info
    lbl_text =  "Available IP Addresses in source net: " + str(total_ips) + "\n"
    lbl_text += "Nets: " + str(nets) + "\n"
    lbl_text += "Hosts: " + str(hosts_entry.get()) + "\n"
    lbl_text += "Total Addresses: " + str(needed_ips) + "\n\n"

    #Subnets Output
    lbl_text += "Subnets List:\n"
    ip_per_net = mask_ips(needed_mask)
    calc_net = ip_to_int(first_net)
    txtbox = int_to_ip(calc_net)+"/"+str(needed_mask)+"\n"
    for i in range(nets):
        calc_net += ip_per_net
        txtbox += int_to_ip(calc_net)+"/"+str(needed_mask)+"\n"

    lbl_result["text"] = lbl_text
    txt_box.insert("1.0",txtbox)


# root window
root = tk.Tk()
root.geometry("500x500")
root.resizable(True, True)
root.title('Subnetting')

ip = tk.StringVar()
nets = tk.StringVar()
hosts = tk.StringVar()

# main frame
subnets = ttk.Frame(root)
subnets.pack(padx=10, pady=10, fill='x', expand=True)

# IP Address
lbl_ip1 = ttk.Label(subnets, text="IP Address/Subnet Mask")
lbl_ip1.pack(fill='x', expand=True)
ip1_entry = ttk.Entry(subnets, textvariable=ip)
ip1_entry.pack(fill='x', expand=True)
ip1_entry.focus()

# Nets
lbl_nets = ttk.Label(subnets, text="Required Networks: ")
lbl_nets.pack(fill='x', expand=True)
nets_entry = ttk.Entry(subnets, textvariable=nets)
nets_entry.pack(fill='x', expand=True)

# Hosts
lbl_hosts = ttk.Label(subnets, text="Required Hosts: ")
lbl_hosts.pack(fill='x', expand=True)
hosts_entry = ttk.Entry(subnets, textvariable=hosts)
hosts_entry.pack(fill='x', expand=True)

# Calculate subnets button
calculate_button = ttk.Button(subnets, text="Calculate Subnets", command=subnets_calc)
calculate_button.pack(fill='x', expand=True, pady=10)

# Info Label
lbl_result = ttk.Label(subnets, text="No Result")
lbl_result.pack(fill='x', expand=True)

# Text Box
txt_box = tk.Text(subnets, height=15, width=40)
txt_box.pack(pady=5)

#for testing
test_data(ip,nets,hosts)

root.mainloop()