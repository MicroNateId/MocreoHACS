# MOCREO IoT Platform Custom Integration for Home Assistant

![Version](https://img.shields.io/github/v/release/MicroNateId/MocreoHACS?style=for-the-badge&color=blue)
![License](https://img.shields.io/github/license/MicroNateId/MocreoHACS?style=for-the-badge&color=green)
![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)

> [!IMPORTANT]
> **DISCLAIMER & LEGAL NOTICE**:
> 1. **Unofficial Integration**: This custom component is an independent, open-source community project. It is **not** created, maintained, supported, affiliated with, or endorsed by MOCREO® or its parent/affiliated entities. All product names, logos, trademarks, and registered trademarks are the property of their respective owners.
> 2. **Provided "AS IS"**: This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, AND NON-INFRINGEMENT.
> 3. **Limitation of Liability**: IN NO EVENT SHALL THE AUTHORS, CONTRIBUTORS, OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
> 4. **No Guarantee of Critical Monitoring**: This software is not intended for high-risk, life-critical, medical, or mission-critical monitoring. The author accepts **zero liability** for any property damage, inventory/food spoilage, equipment failure, business interruption, or missed alerts resulting from the use or failure of this software.

This custom component integrates the **MOCREO IoT Platform** into Home Assistant, enabling local tracking of devices via the MOCREO Cloud Public API.

## Hardware & Product Line Support

This integration dynamically discovers and supports all MOCREO product families:

| Hardware Type | Product Name / Models | Default Icon | Supported Features |
| :--- | :--- | :--- | :--- |
| **Hub / Gateway** | H6Pro, H5-Pro, H5-Lite, H1B, H2 | `mdi:router-wireless` | Online Connectivity Status |
| **Climate Sensor** | LS3, LS3T, ST6, ST3, ST4, ST5 | `mdi:thermometer-water` | Temperature, Humidity, Battery Percentage, Online Status |
| **Water Leak Detector** | SW1, SW2 | `mdi:water-alert` | Moisture Binary Alert, Water Leak State, Battery Percentage, Online Status |
| **Freezer / Cryo Sensor** | ST9, SF1 | `mdi:snowflake-alert` | Ultra-low Temperature (down to -200°C), Frozen State, Battery Percentage, Online Status |
| **Soil Moisture Sensor** | SL1 | `mdi:sprout` | Soil Moisture Level, Battery Percentage, Online Status |
| **Contact / Door Sensor** | SC1 | `mdi:door` | Door/Window Open/Close State, Battery Percentage, Online Status |

## Features

- **Automated Authentication Flow**: Just type in your MOCREO account email and password; the integration will automatically retrieve your assets and generate a secure API Key for Home Assistant.
- **Dynamic Entity Discovery**: Automatically creates sensor and binary sensor entities based on the properties reported by each device.
- **Sensors & Measurements Supported**:
  - **Temperature** (`°C` or `°F`, scaled automatically)
  - **Humidity** (`%`)
  - **Battery Percentage** (`%`)
  - **Water Level**
  - **Water Leak State**
  - **Frozen State**
- **Binary Sensors Supported**:
  - **Online Status** (`Connectivity` binary sensor for all hubs and nodes)
  - **Moisture / Water Leak Alert** (`Moisture` binary sensor for water detectors)
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

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
