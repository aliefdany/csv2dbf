#!/bin/bash

# Define colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Installation paths
INSTALL_DIR="/opt/csv2dbf"
VENV_DIR="$INSTALL_DIR/venv"
BIN_LINK="/usr/local/bin/csv2dbf"

# Function to print error message and exit
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Function to print success message
success_msg() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print info message
info_msg() {
    echo -e "${YELLOW}$1${NC}"
}

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then 
    error_exit "Please run this script with sudo privileges"
fi

# Function to detect Linux distribution
get_distribution() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    else
        echo "unknown"
    fi
}

# Function to install Python and virtualenv
install_requirements() {
    local distro=$1
    info_msg "Installing Python3 and virtualenv..."
    
    case $distro in
        "ubuntu"|"debian")
            apt-get update
            apt-get install -y python3 python3-pip python3-venv
            ;;
        "fedora")
            dnf update -y
            dnf install -y python3 python3-pip python3-virtualenv
            ;;
        "centos"|"rhel")
            yum update -y
            yum install -y python3 python3-pip python3-virtualenv
            ;;
        "opensuse"|"suse")
            zypper refresh
            zypper install -y python3 python3-pip python3-virtualenv
            ;;
        "arch")
            pacman -Sy
            pacman -S --noconfirm python python-pip python-virtualenv
            ;;
        *)
            error_exit "Unsupported distribution for automatic installation"
            ;;
    esac
}

# Main installation process
info_msg "Starting CSV to DBF converter installation..."

# Install Python and virtualenv if needed
distro=$(get_distribution)
info_msg "Detected distribution: $distro"
install_requirements "$distro"

# Create installation directory
info_msg "Creating installation directory..."
mkdir -p "$INSTALL_DIR"

# Copy files to installation directory
info_msg "Copying files..."
cp csv2dbf.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# Create virtual environment
info_msg "Creating virtual environment..."
python3 -m venv "$VENV_DIR"
if [ $? -ne 0 ]; then
    error_exit "Failed to create virtual environment"
fi

# Activate virtual environment and install requirements
info_msg "Installing Python packages in virtual environment..."
source "$VENV_DIR/bin/activate"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt"
deactivate

# Create launcher script
info_msg "Creating launcher script..."
cat > "$BIN_LINK" << 'EOF'
#!/bin/bash
INSTALL_DIR="/opt/csv2dbf"
VENV_DIR="$INSTALL_DIR/venv"

# Activate virtual environment and run script
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/csv2dbf.py" "$@"
deactivate
EOF

# Make launcher script executable
chmod +x "$BIN_LINK"

# Set correct permissions
chown -R root:root "$INSTALL_DIR"
chmod -R 755 "$INSTALL_DIR"

success_msg "Installation completed successfully!"
echo -e "You can now use the converter by running: ${YELLOW}csv2dbf input.csv output.dbf${NC}"
echo -e "For help, run: ${YELLOW}csv2dbf --help${NC}"