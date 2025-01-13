# CSV to DBF Converter

A Python-based command-line tool for converting CSV files to DBF format. This tool runs in an isolated virtual environment and supports various CSV formats and encodings.

## Features

- Convert CSV files to DBF format
- Support for different CSV delimiters
- Custom file encoding support
- Progress tracking for large files
- Isolated virtual environment
- Cross-platform compatibility
- Detailed error reporting

## System Requirements

- Linux-based operating system (Ubuntu, Debian, Fedora, CentOS, RHEL, openSUSE, or Arch Linux)
- Root/sudo privileges for installation

## Installation

1. Download the package files:

   ```bash
   git clone https://github.com/aliefdany/csv2dbf.git
   cd csv2dbf
   ```

2. Make the installation script executable:

   ```bash
   chmod +x install.sh
   ```

3. Run the installation script with sudo:
   ```bash
   sudo ./install.sh
   ```

The installation script will:

- Check and install Python 3 if not present
- Create a virtual environment
- Install all required dependencies
- Set up the command-line tool

## Usage

### Basic Usage

Convert a CSV file to DBF:

```bash
csv2dbf input.csv output.dbf
```

### Advanced Options

```bash
csv2dbf [-h] [-d DELIMITER] [-e ENCODING] [-v] input output
```

Arguments:

- `input`: Input CSV file path
- `output`: Output DBF file path

Optional arguments:

- `-h, --help`: Show help message
- `-d, --delimiter`: CSV delimiter (default: ',')
- `-e, --encoding`: Input file encoding (default: utf-8)
- `-v, --verbose`: Enable verbose output

### Examples

1. Basic conversion:

   ```bash
   csv2dbf data.csv output.dbf
   ```

2. Using semicolon as delimiter:

   ```bash
   csv2dbf -d ';' data.csv output.dbf
   ```

3. Using different encoding:

   ```bash
   csv2dbf -e 'latin-1' data.csv output.dbf
   ```

4. With verbose output:
   ```bash
   csv2dbf -v data.csv output.dbf
   ```

## File Structure

After installation, the files are organized as follows:

```
/opt/csv2dbf/
├── csv2dbf.py
├── requirements.txt
└── venv/
    └── [virtual environment files]

/usr/local/bin/
└── csv2dbf -> [launcher script]
```

## Uninstallation

To remove the package:

```bash
sudo ./uninstall.sh
```

## Troubleshooting

1. If you see "Permission denied":

   ```bash
   sudo chmod +x /usr/local/bin/csv2dbf
   ```

2. If Python packages fail to install:

   ```bash
   sudo /opt/csv2dbf/venv/bin/pip install -r /opt/csv2dbf/requirements.txt
   ```

3. If the converter isn't found in PATH:
   ```bash
   sudo ln -s /opt/csv2dbf/csv2dbf.py /usr/local/bin/csv2dbf
   ```

## Common Issues

1. **"Command not found" error**

   - Ensure the installation completed successfully
   - Check if `/usr/local/bin` is in your PATH
   - Try running the uninstall script and reinstalling

2. **Encoding errors**

   - Try specifying the correct encoding with `-e`
   - Common encodings: 'utf-8', 'latin-1', 'cp1252'

3. **Column name issues**
   - DBF format limits column names to 10 characters
   - Special characters in column names are removed
   - Duplicate column names are modified to be unique

## Support

If you encounter any issues:

1. Run the command with verbose flag (`-v`)
2. Check the error message
3. Verify file permissions and encoding
4. Ensure all dependencies are correctly installed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
