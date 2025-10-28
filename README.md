# Ventilation Control Python

A Python application to control a Stiebel Eltron LWZ 170E plus ventilation system via Raspberry Pi GPIO ports. This application provides a REST API to control the ventilation levels.

## Hardware Requirements

- Raspberry Pi (Zero or other models)
- Stiebel Eltron LWZ 170E plus ventilation system
- GPIO connections:
  - GPIO 17
  - GPIO 22
  - GPIO 27

## GPIO Port Configuration

The ventilation levels are controlled through the following GPIO port configurations:

- OFF: GPIO 17 high, others low
- LOW: All GPIO ports low
- MEDIUM: GPIO 27 high, others low
- HIGH: GPIO 22 high, others low

## Installation

### On Raspberry Pi

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd ventilation-control-python
   ```

2. Install required system packages:
   ```bash
   sudo apt update
   sudo apt install python3-venv python3-dev
   ```

3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Configure pip to use piwheels (pre-compiled wheels for Raspberry Pi):
   ```bash
   # Create or edit pip configuration
   mkdir -p ~/.config/pip
   echo "[global]
   extra-index-url=https://www.piwheels.org/simple" > ~/.config/pip/pip.conf
   ```

4. Install the requirements:
   ```bash
   # Update pip first
   pip install --upgrade pip
   
   # Install requirements using piwheels
   pip install -r requirements.txt
   ```

   Note: The installation will be much faster now as it uses pre-compiled wheels from piwheels.org instead of building from source.

### On Ubuntu (Development/Testing)

1. Make sure Python is installed:
   ```bash
   python3 --version
   ```
   If Python is not installed:
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv
   ```

2. Clone this repository:
   ```bash
   git clone [repository-url]
   cd ventilation-control-python
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages (note: RPi.GPIO will be skipped as it's not needed for mock mode):
   ```bash
   pip install fastapi uvicorn
   ```

The application will automatically run in mock mode when running on Ubuntu.

## Running the Application

### Manual Start

1. Start the server:
   ```bash
   python main.py
   ```

   The server will start on http://0.0.0.0:8000

### Automatic Start on Boot (Raspberry Pi)

The application can be set up to start automatically using a user-level systemd service, which doesn't require root privileges.

To run the application as a user service:

1. Create the user systemd directory if it doesn't exist:
   ```bash
   mkdir -p ~/.config/systemd/user/
   ```

2. Create a symbolic link to the service file (recommended) or copy it:
   ```bash
   # Option A: Create a symbolic link (recommended)
   ln -s $(pwd)/systemd/ventilation-control-user.service ~/.config/systemd/user/ventilation-control.service
   
   # Option B: Copy the file (if you prefer a separate copy)
   # cp systemd/ventilation-control-user.service ~/.config/systemd/user/ventilation-control.service
   ```

3. Reload the user systemd daemon:
   ```bash
   systemctl --user daemon-reload
   ```

4. Enable the service for your user:
   ```bash
   systemctl --user enable ventilation-control
   ```

5. Start the service:
   ```bash
   systemctl --user start ventilation-control
   ```

To enable the service to start on boot (even if user is not logged in):
```bash
sudo loginctl enable-linger $USER
```

You can check the status of the user service with:
```bash
systemctl --user status ventilation-control
```

To view the user service logs:
```bash
journalctl --user -u ventilation-control -f
```

To stop the user service:
```bash
systemctl --user stop ventilation-control
```

To disable automatic start for the user service:
```bash
systemctl --user disable ventilation-control
```

## Mock Mode

The application includes a mock mode for testing on non-Raspberry Pi hardware. Mock mode is automatically activated when:
- Running on non-Raspberry Pi hardware
- Setting the environment variable `VENTILATION_FORCE_MOCK=true`

To force mock mode:
```bash
export VENTILATION_FORCE_MOCK=true
python main.py
```

## API Endpoints

### Get Current Ventilation Level
```
GET /ventilation-control/level
```
Returns the current ventilation level.

Example response:
```json
{
    "level": "medium"
}
```

### Set Ventilation Level
```
POST /ventilation-control/level/{level}
```
Sets the ventilation to the specified level.

Valid levels:
- off
- low
- medium
- high

Example request:
```bash
curl -X POST http://localhost:8000/ventilation-control/level/medium
```

Example response:
```json
{
    "level": "medium",
    "status": "success"
}
```

## Error Handling

The API will return appropriate error messages if:
- An invalid ventilation level is specified
- There are issues with the GPIO hardware

## License

[Add your chosen license here]