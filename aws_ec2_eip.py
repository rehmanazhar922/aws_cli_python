import os, sys
import subprocess

def create_ip():
    create_cmd = subprocess.getoutput("aws ec2 allocate-address")
    create_cmd = create_cmd.splitlines()

    for line in create_cmd:
        if '"AllocationId":' in line:
            allocation_line = line
        else:
            pass

    allocation_line = allocation_line.replace('    "AllocationId": "', "")
    allocation_id = allocation_line.replace('",', "")

    for line in create_cmd:
        if '"PublicIp":' in line:
            create_cmd = line
        else:
            pass

    create_cmd = create_cmd.replace('    "PublicIp": "', "")
    ip = create_cmd.replace('",', "")
    return ip, allocation_id


def release_ip(allocation_id, prnt=False):
    rcmd = subprocess.getoutput(f"aws ec2 release-address --allocation-id {allocation_id}")
    if prnt == True:
        print(f"{ip} has been released")
        print(f"cmd output : {rcmd}")


def assign_ip(allocation_id, Instance_ID):
    do = subprocess.getoutput(f"aws ec2 associate-address --instance-id {Instance_ID}  --allocation-id {allocation_id} ")
    return do


def list_all_ip():
    create_cmd = subprocess.getoutput("aws ec2 describe-addresses")
    create_cmd = create_cmd.splitlines()
    ips = []
    for line in create_cmd:
        if 'PublicIp":' in line:
            line = line.replace('            "PublicIp": "', "")
            line = line.replace('",', "")
            ips.append(line)
    return ips

def list_all_allocation_ids():
    create_cmd = subprocess.getoutput("aws ec2 describe-addresses")
    create_cmd = create_cmd.splitlines()
    ips = []
    for line in create_cmd:
        if 'AllocationId":' in line:
            line = line.replace('            "AllocationId": "', "")
            line = line.replace('",', "")
            ips.append(line)
    return ips


def delete_all_ips():
    ips = list_all_allocation_ids()
    for ip in ips:
        create_cmd = subprocess.getoutput(f"aws ec2 release-address --allocation-id {ip}")
        print(create_cmd)


def list_all_binded_allocation_ids():
    create_cmd = subprocess.getoutput("aws ec2 describe-addresses")
    create_cmd = create_cmd.splitlines()
    ips = []
    line_num = -1
    for line in create_cmd:
        line_num = line_num + 1
        if 'AssociationId":' in create_cmd[line_num]:
            line = create_cmd[line_num-1].replace('            "AllocationId": "', "")
            line = line.replace('",', "")
            ips.append(line)
    return ips


def delete_all_running_ip():
    ips = list_all_binded_allocation_ids()
    for ip in ips:
        create_cmd = subprocess.getoutput(f"aws ec2 release-address --allocation-id {ip}")
        print(create_cmd)


def list_all_not_binded_allocation_ids():
    ips = list_all_allocation_ids()
    not_binded = ips
    for ip in ips:
        create_cmd = subprocess.getoutput(f'aws ec2 describe-addresses --allocation-ids {ip}')

        create_cmd = str(create_cmd)
        if 'AssociationId":' in create_cmd:
            not_binded.remove(ip)
            
    return not_binded


def delete_all_non_binded_ip():
    ips = list_all_not_binded_allocation_ids()
    for ip in ips:
        create_cmd = subprocess.getoutput(f"aws ec2 release-address --allocation-id {ip}")
        print(create_cmd)
