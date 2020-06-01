#!/bin/bash
set -e

ECEL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

OUTPUT_PREFIX="ECEL INSTALLER:"
OUTPUT_ERROR_PREFIX="$OUTPUT_PREFIX ERROR:"

PYTHON_EXEC="python3"

### Helper functions
#
prompt_accepted_Yn() {
    read -r -p "$1 [Y/n] " yn
    case $yn in
        [nN]*) return 1 ;;
        *) return 0 ;;
    esac
}

# Updates
#echo "Running apt-get update"
#apt-get -y update
#echo "Running apt-get upgrade"
#apt-get upgrade

### Check if running as root
#
if [ "$EUID" -ne 0 ]; then
    echo "$OUTPUT_ERROR_PREFIX Please run this installation as root"
    exit 1
fi

### Install dependencies
#
REQUIRED_PROGRAMS="openjdk-8-jdk zlib1g-dev libpng-dev libxtst-dev python3-psutil python3-pip python3-xlib python3-dpkt libappindicator3-1 gir1.2-appindicator3-0.1 tcpdump"
REQUIRED_PYTHON_PACKAGES="schedule autopy netifaces service Image Pyro4 Pillow python-xlib configobj psutil pmw"
REQUIRED_PLUGINS="tshark auditd"

for plugin in $REQUIRED_PLUGINS; do
    plugin_prompt="$plugin is not installed. Do you wish to install it now (ECEL will still run, but the $plugin plugin(s) won't)?"
    if ! command -v $plugin >/dev/null 2>&1 && prompt_accepted_Yn "$plugin_prompt"; then
        REQUIRED_PROGRAMS="$REQUIRED_PROGRAMS $plugin"
    fi
done

echo "$OUTPUT_PREFIX Installing dependecies"
if [ -x "/usr/bin/apt-get" ]; then
    apt-get -y install $REQUIRED_PROGRAMS
elif [ -x "/usr/bin/yum" ]; then
    yum install -y $REQUIRED_PROGRAMS
else
    echo "$OUTPUT_ERROR_PREFIX Distribution not supported"
    exit 1
fi

echo "$OUTPUT_PREFIX Installing python dependencies"
$PYTHON_EXEC -m pip install pip --upgrade
$PYTHON_EXEC -m pip install $REQUIRED_PYTHON_PACKAGES

if prompt_accepted_Yn "Snoopy logs all system calls. ECEL will still run without it, but the snoopy plugin will not work. Install? "; then
    bash "$ECEL_DIR"/scripts/install-snoopy.sh
fi

### Create plugin configs
# #TODO: do this every time it's necessary
for plugin in "$ECEL_DIR"/plugins/collectors/*; do
    if [ -d "$plugin" ]; then
        if [ ! -f "$plugin"/config.json ]; then
            scp "$plugin"/config.json.template "$plugin"/config.json
        fi
         if [ ! -f "$plugin"/config_schema.json ]; then
            scp "$plugin"/config_schema.json.template "$plugin"/config_schema.json
        fi
    fi
done

### Compile parsers
#
echo "$OUTPUT_PREFIX Compiling parsers" #TODO: Compile new plugins
for plugin in "$ECEL_DIR"/plugins/parsers/*; do
    if [ -d "$plugin" ] && ls "$plugin"/*.java > /dev/null 2>&1; then
        javac "$plugin"/*.java
    fi
done

javac -cp $ECEL_DIR/plugins/parsers/nmap/java_classes/*.java

### Set file permissions
#
echo "$OUTPUT_PREFIX Setting file permissions"
find ./ -name "*.sh" -exec chmod +x {}  \;
chmod +x "$ECEL_DIR"/eceld_service.py

echo "$OUTPUT_PREFIX Installation Complete"
