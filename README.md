# MOCREO IoT Platform Custom Integration for Home Assistant

This custom component integrates the **MOCREO IoT Platform** into Home Assistant, enabling local tracking of devices (such as the H6Pro gateway and LS3T sensors) via the MOCREO Cloud Public API.

## Features

- **Automated Authentication Flow**: Just type in your MOCREO account email and password; the integration will automatically retrieve your assets and generate a secure API Key for Home Assistant.
- **Dynamic Entity Discovery**: Automatically creates sensor entities based on the capabilities of each device associated with your asset.
- **Sensors Supported**:
  - **Temperature** (`°C` or `°F`, converted automatically by Home Assistant settings)
  - **Humidity** (`%`)
  - **Battery Percentage** (`%`)
- **Binary Sensors Supported**:
  - **Online Status** (`Connectivity` binary sensor for both gateways and nodes)
- **Automatic Refresh**: Automatically polls the MOCREO API every 60 seconds.

## Installation

### Method 1: HACS (Recommended)
You can install this integration via the Home Assistant Community Store (HACS):
1. In Home Assistant, open **HACS** and go to the **Integrations** section.
2. Click the three dots in the top-right corner and select **Custom repositories**.
3. Add the following GitHub repository URL:
   ```text
   https://github.com/MicroNateId/MocreoHACS
   ```
4. Select **Integration** as the category, and click **Add**.
5. Find **MOCREO IoT Platform** in the search list, click it, and select **Download**.
6. Restart Home Assistant.

### Method 2: Manual Installation
1. Download or copy the `custom_components/mocreo` directory from this repository.
2. Place the `mocreo` folder inside your Home Assistant config directory's `custom_components` folder:
   ```text
   config/
   └── custom_components/
       └── mocreo/
           ├── __init__.py
           ├── binary_sensor.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           └── translations/
               └── en.json
   ```
3. Restart Home Assistant.

## Configuration

1. In the Home Assistant UI, navigate to **Settings** -> **Devices & Services**.
2. Click **Add Integration** in the bottom right corner.
3. Search for **MOCREO IoT Platform** and select it.
4. Enter your login credentials:
   - **Email**: Your MOCREO login email
   - **Password**: Your MOCREO login password
5. Click **Submit**. 
   * If you have only one Asset, the integration will auto-select it, generate an API Key, and finish setup.
   * If you have multiple Assets, you will be prompted with a dropdown to select which asset/location you want to sync.
6. The integration will automatically load all your devices!
