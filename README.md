# hope
HouseOfagile Open Protection Engine: A comprehensive, open-source Linux security auditing and protection tool.

# README

### System Security Checker

This Python script helps in performing various security checks on your system, including log analysis, checking network connections, identifying backdoors, and using popular security tools like Lynis, chkrootkit, rkhunter, and ClamAV.

#### Requirements

- Python 3.x
- The following tools must be installed if you plan to use them:
  - `lynis`
  - `chkrootkit`
  - `rkhunter`
  - `clamav`
- `PyYAML`, `tqdm`, and `termcolor` libraries are required for handling configuration files, progress bar, and colored output.

#### Installation

1. **Clone the repository** (if applicable):
   ```sh
   git clone [https://github.com/HouseOfAgile/hope.git](https://github.com/HouseOfAgile/hope.git)
   cd hope
   ```

2. **Create a virtual environment** (recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Make the script executable**:
   ```sh
   chmod +x system_security_checker.py
   ```

#### Configuration

The script uses a `package_manager.yml` file to determine which package manager commands to use based on the Linux distribution. This allows the script to be more flexible and work with various distributions, such as Ubuntu, CentOS, and others.

**Example `package_manager.yml`**:

```yaml
default:
  install: "sudo apt-get install -y"
  uninstall: "sudo apt-get remove -y"
ubuntu:
  install: "sudo apt-get install -y"
  uninstall: "sudo apt-get remove -y"
centos:
  install: "sudo yum install -y"
  uninstall: "sudo yum remove -y"
fedora:
  install: "sudo dnf install -y"
  uninstall: "sudo dnf remove -y"
arch:
  install: "sudo pacman -S --noconfirm"
  uninstall: "sudo pacman -R --noconfirm"
```

#### Usage

Run the script with the desired options:

```sh
sudo ./system_security_checker.py [options]
```

#### Options

- `--ssh-logs` - Check SSH logs for suspicious activity.
- `--network` - Check active network connections and listening ports.
- `--suid-sgid` - Check for files with SUID/SGID bits set.
- `--crontab` - Check crontab entries for all users.
- `--lynis` - Run Lynis audit.
- `--chkrootkit` - Run chkrootkit.
- `--rkhunter` - Run rkhunter.
- `--clamav` - Run ClamAV scan.
- `--ping` - Perform ping analysis.
- `--install <tools>` - Install specified tools (`lynis`, `chkrootkit`, `rkhunter`, `clamav`).
- `--uninstall <tools>` - Uninstall specified tools (`lynis`, `chkrootkit`, `rkhunter`, `clamav`).
- `--all` - Run all security checks.
- `--interactive` - Run the script in interactive mode to select which checks to perform.

**Example**:

To check SSH logs and network connections, run:

```sh
sudo ./system_security_checker.py --ssh-logs --network
```

To run all checks:

```sh
sudo ./system_security_checker.py --all
```

To install Lynis and chkrootkit:

```sh
sudo ./system_security_checker.py --install lynis chkrootkit
```

To use interactive mode:

```sh
sudo ./system_security_checker.py --interactive
```

#### Using Virtual Environments

It is recommended to use a virtual environment to avoid conflicts with system packages. You can use `venv` as shown above. Alternatively, you can use other environment managers like `virtualenv`:

- **Using `virtualenv`**:
  ```sh
  pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  ```

#### Recommendations

- **Run as Root**: Some commands require elevated privileges, so it's recommended to run the script with `sudo`.
- **Keep Tools Updated**: Ensure `lynis`, `chkrootkit`, `rkhunter`, and `clamav` are up to date for effective security checks.

#### Disclaimer

This script is intended for educational purposes and basic diagnostics. It may not detect sophisticated threats or fully secure your system. For critical environments, consult a security professional.

#### License

MIT License

Copyright (c) 2024 HouseOfAgile

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
