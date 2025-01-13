#!/bin/bash

# Define colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Installation paths
INSTALL_DIR="/opt/csv2dbf"
BIN_LINK="/usr/local/bin/csv2dbf"

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: Please run this script with sudo privileges${NC}" >&2
    exit 1
fi

echo -e "${YELLOW}Uninstalling CSV to DBF converter...${NC}"

# Remove binary link
if [ -L "$BIN_LINK" ]; then
    rm "$BIN_LINK"
    echo "Removed launcher script"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed installation directory"
fi

echo -e "${GREEN}Uninstallation completed successfully!${NC}"