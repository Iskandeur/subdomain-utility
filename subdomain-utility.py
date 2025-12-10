import socket
from ipwhois import IPWhois
import csv
import subprocess
import os
import sys
import argparse

def run_sublist3r(domain, sublist3r_path='sublist3r.py', output_file=None):
    if not os.path.isfile(sublist3r_path):
        print(f"Error: '{sublist3r_path}' not found.")
        sys.exit(1)
    command = ['python', sublist3r_path, '-d', domain]
    if output_file:
        command += ['-o', output_file]
    try:
        print(f"Running Sublist3r for domain: {domain}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("An error occurred while running Sublist3r.")
        sys.exit(1)

def read_domains(file):
    with open(file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    return domains

def resolve_ip(domain):
    try:
        infos = socket.getaddrinfo(domain, None)
        ips = list(set([info[4][0] for info in infos]))
        return ips
    except socket.gaierror:
        print(f"Resolution error for domain: {domain}")
        return []

def get_host(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap(asn_methods=["whois"])
        org = results.get('network', {}).get('name', 'Unknown')
        return org
    except Exception:
        return "Unknown"

def generate_csv(results, output_file):
    unique_results = []
    seen = set()
    for res in results:
        res_tuple = (res['Domain'], res['Subdomain'], res['IP Address'], res['Host'])
        if res_tuple not in seen:
            seen.add(res_tuple)
            unique_results.append(res)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Domain', 'Subdomain', 'IP Address', 'Host']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for res in unique_results:
            writer.writerow(res)

def main():
    parser = argparse.ArgumentParser(description='Subdomain enumeration and WHOIS lookup tool')
    parser.add_argument('domain', help='Target domain to enumerate subdomains for')
    parser.add_argument('--sublist3r-path', default='Sublist3r/sublist3r.py', help='Path to the sublist3r.py script')
    parser.add_argument('--output', default='host_results.csv', help='Output CSV file for results')
    args = parser.parse_args()

    domain = args.domain
    sublist3r_path = args.sublist3r_path
    output_file = args.output
    subdomains_output_file = 'subdomains.txt'

    run_sublist3r(domain, sublist3r_path, subdomains_output_file)

    domains = read_domains(subdomains_output_file)
    if domain not in domains:
        domains.append(domain)
    results = []

    for domain_item in domains:
        print(f"Processing domain: {domain_item}")
        ips = resolve_ip(domain_item)
        if not ips:
            results.append({
                'Domain': domain_item,
                'Subdomain': '',
                'IP Address': 'Unresolved',
                'Host': 'Unknown'
            })
            continue
        for ip in ips:
            host = get_host(ip)
            parts = domain_item.split('.')
            if len(parts) > 2:
                subdomain = '.'.join(parts[:-2])
                main_domain = '.'.join(parts[-2:])
            else:
                subdomain = ''
                main_domain = domain_item
            results.append({
                'Domain': main_domain,
                'Subdomain': subdomain,
                'IP Address': ip,
                'Host': host
            })

    sorted_results = sorted(results, key=lambda x: x['Host'])
    generate_csv(sorted_results, output_file)
    print(f"Results have been saved to {output_file}")

if __name__ == "__main__":
    main()
