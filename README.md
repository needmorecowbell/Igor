# Igor



<p align="center">
    <img src="https://user-images.githubusercontent.com/7833164/58334823-4db72180-7e0e-11e9-8103-5cbbe32784f9.gif"></img>
</p>

## THIS IS A WORK IN PROGRESS, NOT FULLY DEVELOPED

## What is this?

Igor is a networking tool that requires no external dependencies. Scan your network for other computers, find open ports, and get information about them. This tool doubles as a worm that can attempt to spread through the network of identified machines.

## Setup
No setup needed, just have python3 installed and callable on the system, then grab the file.

` curl https://raw.githubusercontent.com/needmorecowbell/Igor/master/igor.py`


## Usage

```
usage: igor.py [-h] [-w] [-m] [-p] [--who] [-v] [-o FILE]

optional arguments:
  -h, --help           show this help message and exit
  -w, --worm           sets Igor into worm mode
  -m, --map            return ips in local network
  -p, --pscan          return port scan of ips in local network
  --who                return useful notes about the executing system
  -v, --verbose        increase output verbosity
  -o FILE, --out FILE  write results to FILE
  ```

## Example Output

**Input:** `python3 igor.py --who`

**Output:**

```

██╗ ██████╗  ██████╗ ██████╗
██║██╔════╝ ██╔═══██╗██╔══██╗
██║██║  ███╗██║   ██║██████╔╝
██║██║   ██║██║   ██║██╔══██╗
██║╚██████╔╝╚██████╔╝██║  ██║
╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝


Local IP: 10.0.0.33
Public IP: 75.43.12.21

Hostname: micasa
Operating System: posix
Platform: darwin
```
