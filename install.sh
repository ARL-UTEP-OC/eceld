#!/bin/bash
set -e

ECEL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

OUTPUT_PREFIX="ECEL INSTALLER:"
OUTPUT_ERROR_PREFIX="$OUTPUT_PREFIX ERROR:"

PYTHON_EXEC="python3"

VENV_DIR="$ECEL_DIR/.eceld"

### Helper functions
#
prompt_accepted_Yn() {
    read -r -p "$1 [Y/n] " yn
    case $yn in
        [nN]*) return 1 ;;
        *) return 0 ;;
    esac
}

### Check if running as root
#
if [ "$EUID" -ne 0 ]; then
    echo "$OUTPUT_ERROR_PREFIX Please run this installation as root"
    exit 1
fi

# Updates
echo "Running apt-get update"
apt-get -y update
#echo "Running apt-get upgrade"
#apt-get upgrade

### Install dependencies
#
REQUIRED_PROGRAMS="openjdk-11-jdk zlib1g-dev libpng-dev libxtst-dev libgcc-14-dev python3-pip python3-xlib tcpdump python3-psutil" #python3-dpkt 
REQUIRED_PYTHON_PACKAGES="schedule autopy netifaces service Image Pyro4 Pillow python-xlib configobj psutil pmw jinja2"
REQUIRED_PLUGINS="tshark auditd"

for plugin in $REQUIRED_PLUGINS; do
    plugin_prompt="$plugin is not installed. Install it now (ECEL will still run, but the $plugin plugin(s) won't)?"
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

if [ ! -d $VENV_DIR ]; then
    echo "$OUTPUT_PREFIX Creating python environment: $VENV_DIR"
    $PYTHON_EXEC -m venv $VENV_DIR
fi
echo "$OUTPUT_PREFIX Activating python environment: $VENV_DIR"
source $VENV_DIR/bin/activate

$PYTHON_EXEC -m pip install pip --upgrade
$PYTHON_EXEC -m pip install $REQUIRED_PYTHON_PACKAGES

### Create plugin configs
#
for plugin in "$ECEL_DIR"/plugins/collectors/*; do
    #python3 creates temporary directories; this is in case they exist from a previous install
    if [[ "$plugin" == *"__pycache__" ]]; then
        continue
    fi

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
chmod +x "$ECEL_DIR"/eceld_service
echo "$OUTPUT_PREFIX Installation Complete"
