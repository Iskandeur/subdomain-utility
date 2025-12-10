# Subdomain Enumeration and WHOIS Lookup Tool

## Description

This Python script automates the process of:

- Enumerating subdomains for a given domain using [Sublist3r](https://github.com/aboul3la/Sublist3r).
- Resolving IP addresses for each discovered subdomain.
- Performing WHOIS lookups on those IP addresses to gather hosting information.
- Compiling the results into a CSV file for easy analysis.

This tool is useful for penetration testers, security researchers, and network administrators who need to map out subdomains and associated hosting details for a target domain.

## Features

- **Subdomain Enumeration**: Leverages Sublist3r to find subdomains quickly.
- **IP Resolution**: Resolves each subdomain to its corresponding IP address(es).
- **WHOIS Lookup**: Retrieves hosting organization information for each IP address.
- **CSV Output**: Generates a structured CSV file containing all the collected data.

## Installation

### Prerequisites

- Python 3.x
- Git

### Clone This Repository

```bash
git clone https://github.com/Iskandeur/subdomain-utility.git
cd subdomain-utility
```

### Install Sublist3r

The script depends on Sublist3r for subdomain enumeration. Clone the Sublist3r repository:

```bash
git clone https://github.com/aboul3la/Sublist3r.git
```

### Install Python Dependencies

Install the required Python packages using `pip`:

```bash
pip install ipwhois
```

Alternatively, if you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```
ipwhois
```

## Usage

```bash
python subdomain-utility.py <domain> [--sublist3r-path SUBLIST3R_PATH] [--output OUTPUT]
```

### Positional Arguments

- `<domain>`: Target domain to enumerate subdomains for (e.g., `example.com`).

### Optional Arguments

- `--sublist3r-path`: Path to the `sublist3r.py` script. Default is `Sublist3r/sublist3r.py`.
- `--output`: Output CSV file for results. Default is `host_results.csv`.

### Example

Enumerate subdomains for `example.com` and save results to `results.csv`:

```bash
python subdomain-utility.py example.com --output results.csv
```

## Output

The script generates a CSV file containing the following columns:

- **Domain**: The main domain (e.g., `example.com`).
- **Subdomain**: The subdomain part (e.g., `blog` in `blog.example.com`).
- **IP Address**: The resolved IP address of the subdomain.
- **Host**: The hosting organization's name retrieved from WHOIS data.

**Sample Output (`results.csv`):**

| Domain       | Subdomain | IP Address   | Host               |
|--------------|-----------|--------------|--------------------|
| example.com  | www       | 93.184.216.34| Example Organization|
| example.com  |           | 93.184.216.34| Example Organization|
| example.com  | blog      | 93.184.216.35| Example Organization|

## Error Handling

- **Sublist3r Not Found**: If the specified `sublist3r.py` script is not found, the script will exit with an error message.
- **DNS Resolution Failure**: If a subdomain cannot be resolved to an IP address, it will be marked as "Unresolved" in the output.
- **WHOIS Lookup Failure**: If WHOIS data cannot be retrieved for an IP address, the host will be marked as "Unknown".

## Troubleshooting

- Ensure that the Sublist3r path provided is correct and that you have the necessary permissions to execute it.
- Check your network connection if the script fails to resolve domain names or perform WHOIS lookups.

## Acknowledgements

- [Sublist3r](https://github.com/aboul3la/Sublist3r): For efficient subdomain enumeration.
- [IPWhois Library](https://pypi.org/project/ipwhois/): For retrieving WHOIS data for IP addresses.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
