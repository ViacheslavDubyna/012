# Installation and Launch Guide for the National Guard of Ukraine Information and Analytical System

This guide provides detailed instructions for installing and launching the Information and Analytical System of the National Guard of Ukraine.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing PostgreSQL](#installing-postgresql)
3. [Installing Python and Dependencies](#installing-python-and-dependencies)
4. [System Configuration](#system-configuration)
5. [Launching the System](#launching-the-system)
6. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- Operating System: Windows 10/11, Linux (Ubuntu 20.04 or newer), macOS 10.15 or newer
- Processor: 2 cores, 2 GHz
- RAM: 4 GB
- Free disk space: 2 GB
- Internet connection

### Recommended Requirements

- Processor: 4 cores, 3 GHz
- RAM: 8 GB
- Free disk space: 5 GB

### Software

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Modern web browser (Google Chrome, Mozilla Firefox, Microsoft Edge)

## Installing PostgreSQL

### Windows

1. Download the PostgreSQL installer from the official website: https://www.postgresql.org/download/windows/
2. Run the installer and follow the instructions:
   - Select components to install (PostgreSQL Server, pgAdmin, Command Line Tools)
   - Specify the installation directory
   - Set a password for the `postgres` user (remember it!)
   - Specify the port (default is 5432)
   - Select locale
3. After installation, make sure the PostgreSQL service is running:
   - Open "Services" through Control Panel or run `services.msc`
   - Find the PostgreSQL service and make sure it's running

### Linux (Ubuntu)

1. Update the package index:
   ```bash
   sudo apt update
   ```

2. Install PostgreSQL:
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

3. Check the service status:
   ```bash
   sudo systemctl status postgresql
   ```

4. If the service is not running, start it:
   ```bash
   sudo systemctl start postgresql
   ```

5. Set a password for the `postgres` user:
   ```bash
   sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
   ```

### macOS

1. Install Homebrew if it's not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install PostgreSQL:
   ```bash
   brew install postgresql
   ```

3. Start PostgreSQL:
   ```bash
   brew services start postgresql
   ```

4. Set a password for the `postgres` user:
   ```bash
   psql postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"
   ```

## Installing Python and Dependencies

### Windows

1. Download the Python installer from the official website: https://www.python.org/downloads/
2. Run the installer and follow the instructions:
   - Check the option "Add Python to PATH"
   - Select "Install Now"
3. Verify the Python installation by opening a command prompt and running:
   ```bash
   python --version
   ```

### Linux (Ubuntu)

1. Install Python and pip:
   ```bash
   sudo apt install python3 python3-pip
   ```

2. Verify the installation:
   ```bash
   python3 --version
   pip3 --version
   ```

### macOS

1. Install Python using Homebrew:
   ```bash
   brew install python
   ```

2. Verify the installation:
   ```bash
   python3 --version
   pip3 --version
   ```

## System Configuration

1. Clone or unpack the system archive to a convenient directory.

2. Open a command prompt or terminal and navigate to the system directory:
   ```bash
   cd path/to/directory/ias_military
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Open the `config/config.py` file and check the database settings:
   ```python
   DB_CONFIG = {
       'user': 'postgres',
       'password': 'postgres',  # Change to your password if it's different
       'host': 'localhost',
       'port': '5432',
       'database': 'ngu_ias'
   }
   ```

   Change the `'password'` value to the password you set for the `postgres` user during PostgreSQL installation.

## Launching the System

### Full System Launch

To fully launch the system (PostgreSQL setup, database initialization, test data seeding, and web interface launch), run the command:

```bash
python start_system.py
```

The system will automatically perform all necessary steps and open the web interface in your browser.

### Launch with Additional Options

You can use additional options to skip certain launch stages:

- `--skip-db-setup` - skip PostgreSQL setup
- `--skip-db-init` - skip database initialization
- `--skip-db-seed` - skip test data seeding

For example, if you have already set up the database and only want to launch the web interface:

```bash
python start_system.py --skip-db-setup --skip-db-init --skip-db-seed
```

### Launching Individual Components

If you need to launch only specific system components, you can use the following commands:

1. PostgreSQL setup:
   ```bash
   python setup_postgres.py
   ```

2. Database initialization:
   ```bash
   python run.py init_db
   ```

3. Test data seeding:
   ```bash
   python run.py seed_db
   ```

4. Web interface launch:
   ```bash
   python run.py
   ```

## Troubleshooting

### PostgreSQL Doesn't Start

1. Check if PostgreSQL is installed:
   - Windows: Check for the PostgreSQL service in the services list
   - Linux: `sudo systemctl status postgresql`
   - macOS: `brew services list | grep postgresql`

2. Check if the PostgreSQL service is running:
   - Windows: Start the service through "Services"
   - Linux: `sudo systemctl start postgresql`
   - macOS: `brew services start postgresql`

3. Check firewall settings:
   - Make sure port 5432 is open for local connections

### Database Connection Error

1. Check the settings in the `config/config.py` file:
   - Verify the username, password, host, and port

2. Check if the `ngu_ias` database exists:
   - Connect to PostgreSQL: `psql -U postgres`
   - View the list of databases: `\l`

3. If the database doesn't exist, create it manually:
   - `CREATE DATABASE ngu_ias;`

### Dependency Installation Error

1. Update pip to the latest version:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Install dependencies one by one to identify the problematic package:
   ```bash
   pip install flask==2.3.3
   pip install sqlalchemy==2.0.23
   # etc.
   ```

3. For Windows, you may need to install a C++ compiler:
   - Download and install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Web Interface Doesn't Open

1. Check if the web server is running:
   - There should be a message about server startup in the console

2. Check the address in the browser:
   - Default: http://localhost:5000

3. Check if the firewall is blocking port 5000:
   - Temporarily disable the firewall or add an exception for port 5000

4. Try using a different browser

### Other Issues

If you encounter other issues, try:

1. Restart the system with a clean database:
   ```bash
   python start_system.py
   ```

2. Check the error logs in the console

3. Contact the system developers with a detailed description of the problem and steps to reproduce it