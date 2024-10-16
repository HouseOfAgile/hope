#!/usr/bin/env python3
import argparse
import os
import subprocess
import platform
import distro
import shutil
import yaml
import tempfile
import datetime
from tqdm import tqdm
from termcolor import colored

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}': {e.stderr.decode('utf-8')}"

def load_package_manager():
    with open("package_manager.yml", "r") as f:
        config = yaml.safe_load(f)
    import distro
    distro = distro.id().lower()
    return config.get(distro, config["default"])

def install_tool(tool_name, package_manager):
    print(f"\n=== Installing {tool_name} ===")
    result = run_command(f"{package_manager['install']} {tool_name}")
    print(result)

def uninstall_tool(tool_name, package_manager):
    print(f"\n=== Uninstalling {tool_name} ===")
    result = run_command(f"{package_manager['uninstall']} {tool_name}")
    print(result)

def check_ssh_logs():
    print(colored("\n=== Checking SSH Logs ===", "yellow"))
    if platform.system() == "Linux":
        auth_log = "/var/log/auth.log" if os.path.exists("/var/log/auth.log") else "/var/log/secure"
        failed_attempts = run_command(f"grep 'Failed password' {auth_log} | tail -20")
        usernames = run_command(f"grep 'Failed password' {auth_log} | awk '{{print $9}}' | sort | uniq -c")
        last_logins = run_command(f"last -a | head -10")
        print(failed_attempts)
        print(colored("\n=== SSH Username Requests ===", "cyan"))
        print(usernames)
        print(colored("\n=== Last Login Attempts ===", "cyan"))
        print(last_logins)
    else:
        print("SSH log checking is not supported on this platform.")

def check_network_connections():
    print(colored("\n=== Active Network Connections and Listening Ports ===", "yellow"))
    command = "netstat -tulpn" if shutil.which("netstat") else "ss -tulpn"
    result = run_command(command)
    print(result)

def check_suid_sgid_files():
    print(colored("\n=== Checking for Files with SUID/SGID Bits Set ===", "yellow"))
    result = run_command("find / -perm /6000 -type f 2>/dev/null")
    print(result)

def check_crontab():
    print(colored("\n=== Checking Crontab Entries for All Users ===", "yellow"))
    users = [line.split(':')[0] for line in open('/etc/passwd')]
    for user in users:
        result = run_command(f"crontab -u {user} -l 2>/dev/null")
        if result:
            print(f"--- Crontab for {user} ---\n{result}")

def ping_analysis():
    print(colored("\n=== Performing Ping Analysis ===", "yellow"))
    hosts = ["8.8.8.8", "8.8.4.4"]  # Google DNS servers
    for host in hosts:
        result = run_command(f"ping -c 4 {host}")
        print(f"--- Ping results for {host} ---\n{result}")

def run_lynis():
    print(colored("\n=== Running Lynis Audit ===", "yellow"))
    if shutil.which("lynis"):
        result = run_command("sudo lynis audit system")
        print(result)
    else:
        print("Lynis is not installed.")

def run_chkrootkit():
    print(colored("\n=== Running chkrootkit ===", "yellow"))
    if shutil.which("chkrootkit"):
        result = run_command("sudo chkrootkit")
        print(result)
    else:
        print("chkrootkit is not installed.")

def run_rkhunter():
    print(colored("\n=== Running rkhunter ===", "yellow"))
    if shutil.which("rkhunter"):
        result = run_command("sudo rkhunter --check")
        print(result)
    else:
        print("rkhunter is not installed.")

def run_clamav():
    print(colored("\n=== Running ClamAV Scan ===", "yellow"))
    if shutil.which("clamscan"):
        result = run_command("sudo clamscan -r / --infected --remove")
        print(result)
    else:
        print("ClamAV is not installed.")

def interactive_mode():
    print(colored("\n=== Interactive Mode ===", "yellow"))
    tools = [
        ("Check SSH logs", check_ssh_logs),
        ("Check network connections", check_network_connections),
        ("Check SUID/SGID files", check_suid_sgid_files),
        ("Check crontab entries", check_crontab),
        ("Ping analysis", ping_analysis),
        ("Run Lynis audit", run_lynis),
        ("Run chkrootkit", run_chkrootkit),
        ("Run rkhunter", run_rkhunter),
        ("Run ClamAV scan", run_clamav)
    ]
    for idx, (name, _) in enumerate(tools, 1):
        print(f"{idx}. {name}")
    choices = input("Enter the numbers of the checks to run (comma-separated, or 'all' for all checks): ").strip()
    if choices.lower() == 'all':
        for _, func in tqdm(tools, desc="Running All Checks"):
            func()
    else:
        try:
            selected = [int(x) for x in choices.split(',')]
            for idx in tqdm(selected, desc="Running Selected Checks"):
                if 1 <= idx <= len(tools):
                    tools[idx - 1][1]()
                else:
                    print(f"Invalid choice: {idx}")
        except ValueError:
            print("Invalid input. Please enter numbers or 'all'.")

def main():
    parser = argparse.ArgumentParser(description="System Security Checker Script")
    parser.add_argument("--ssh-logs", action="store_true", help="Check SSH logs for suspicious activity")
    parser.add_argument("--network", action="store_true", help="Check active network connections and listening ports")
    parser.add_argument("--suid-sgid", action="store_true", help="Check for files with SUID/SGID bits set")
    parser.add_argument("--crontab", action="store_true", help="Check crontab entries for all users")
    parser.add_argument("--lynis", action="store_true", help="Run Lynis audit")
    parser.add_argument("--chkrootkit", action="store_true", help="Run chkrootkit")
    parser.add_argument("--rkhunter", action="store_true", help="Run rkhunter")
    parser.add_argument("--clamav", action="store_true", help="Run ClamAV scan")
    parser.add_argument("--ping", action="store_true", help="Perform ping analysis")
    parser.add_argument("--install", nargs='+', help="Install specified tools (lynis, chkrootkit, rkhunter, clamav)")
    parser.add_argument("--uninstall", nargs='+', help="Uninstall specified tools (lynis, chkrootkit, rkhunter, clamav)")
    parser.add_argument("--all", action="store_true", help="Run all security checks")
    parser.add_argument("--all-install", action="store_true", help="Install all required tools and run all security checks")
    parser.add_argument("--interactive", action="store_true", help="Run the script in interactive mode")
    
    args = parser.parse_args()

    package_manager = load_package_manager()

    if args.install:
        for tool in args.install:
            install_tool(tool, package_manager)

    if args.uninstall:
        for tool in args.uninstall:
            uninstall_tool(tool, package_manager)

    if args.all:
        for func in tqdm([check_ssh_logs, check_network_connections, check_suid_sgid_files, check_crontab, ping_analysis, run_lynis, run_chkrootkit, run_rkhunter, run_clamav], desc="Running All Checks"):
            func()

    if args.all_install:
            tools = ['lynis', 'chkrootkit', 'rkhunter', 'clamav']
            for tool in tools:
                install_tool(tool, package_manager)
            for func in tqdm([check_ssh_logs, check_network_connections, check_suid_sgid_files, check_crontab, ping_analysis, run_lynis, run_chkrootkit, run_rkhunter, run_clamav], desc="Installing Tools and Running All Checks"):
                func()
            func()

    if args.interactive:
        interactive_mode()

    if args.ssh_logs:
        check_ssh_logs()
    if args.network:
        check_network_connections()
    if args.suid_sgid:
        check_suid_sgid_files()
    if args.crontab:
        check_crontab()
    if args.ping:
        ping_analysis()
    if args.lynis:
        run_lynis()
    if args.chkrootkit:
        run_chkrootkit()
    if args.rkhunter:
        run_rkhunter()
    if args.clamav:
        run_clamav()

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()