from .tasks import nmap_analyze

def start_nmap_analyze(valid_data):
    subnet_ip = valid_data["subnet_ip"]
    mask = valid_data["mask"]

    nmap_analyze.delay(subnet_ip, mask)