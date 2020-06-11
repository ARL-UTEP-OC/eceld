# Evaluator-Centric and Extensible Logger (ECEL)

## System Requirements
ECEL has been tested on:
* Kali Linux 2019.2, 2020.2 16-bit
* Ubuntu 16.04 LTS, 18.04 LTS, 20.04 LTS 64-bit

## Installation
To install ECEL, run `./install.sh`. A internet connection is required for installation.

## Execution
1. Run `./ecel_service` to execute ECELd. 

2. You can then run the test script `python3 test_engine_invoke.py` to ensure everything runs correctly.

## Plugins

The ECEL is written using a plugin architecture. There are two types of plugins, collectors and parsers. Collector plugins will collect timestamps and event data. These collector plugins use custom or existing external
logging tools. Parser plugins read log data (that produced by the collectors) and then format the data into an alternate form. All plugins are managed (started, terminated, etc.) from the ECEL graphical interface. Additionally the JSON parsers all have at least these  keys: timestamp and start. 

The following are the plugins that come packaged with ECEL.

### PyKeylogger

Forked from: https://github.com/nanotube/pykeylogger

The collector plugin will execute pykeylogger to gather screenshots (on mouse clicks on based on a timer) and keystrokes.
The parser plugin executes three tasks. The first will read keystroke data and then, based on a time threshold/delimiter, weave the data into keystroke units and produce a labeled JSON file.
The second extracts mouse click screenshot paths and timestamps and stores them in a JSON file. Simiarly, the last task extracts timed screenshot paths and timestamps and stores them in a JSON file.

### tshark

https://www.wireshark.org/download.html

By default, this will collect network data on all interfaces, except any specified in the config.json file. Under the hood, this plugin uses tcpdump for collection and tshark for parsing.
The parser plugin will extract various protocol fields from network packtes including source and destination MAC, IP, and port information as well as flags (TCP) and routes (RIP).

### Auditd

https://linux.die.net/man/8/auditd

This plugin collects system calls (execve) using the auditd service. By default, the auditd config file (/etc/auditd.conf) is modified to save logs into the plugin's raw folder.
The parser plugin will read the logs and generate a set of timestamp/system call pairs formatted in a JSON file.

### Nmap

https://nmap.org/

This plugin continually runs the nmap command (by default against the localhost). The purpose of this plugin is to help keep track of network connectivity.
The parser will read the generated log (in XML format) and convert it to JSON.
