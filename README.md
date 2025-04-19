# 🗑️ IoT Smart Garbage Separator

A MicroPython-based IoT project that automatically sorts waste into recyclable, non-recyclable, and organic categories using computer vision and mechanical sorting.

## 🌟 Features

- 🤖 **Automatic Waste Detection**: Uses IR sensors to detect incoming waste
- 👁️ **Computer Vision**: Captures and analyzes waste using a camera
- 🧠 **AI Classification**: Utilizes Google's Gemini API for waste categorization
- 🔄 **Mechanical Sorting**: Automatically sorts waste into appropriate bins
- 📱 **User Interface**: LCD display for real-time status updates
- 💡 **Visual Feedback**: NeoPixel LEDs for system status indication
- 🌐 **IoT Connectivity**: WiFi-enabled for remote monitoring and updates

## 🛠️ Hardware Components

- ESP32 Microcontroller
- Camera Module
- IR Sensor
- 4 Servo Motors
- Stepper Motor
- 16x NeoPixel LED Ring
- 4x20 LCD Display
- WiFi Module

### 🔌 Pin Connections

| Component | Pin Number | Description |
|-----------|------------|-------------|
| **Servo Motors** | | |
| Front Servo 1 | GPIO 9 | Front sorting mechanism |
| Front Servo 2 | GPIO 8 | Front sorting mechanism |
| Drop Servo 1 | GPIO 7 | Drop mechanism |
| Drop Servo 2 | GPIO 44 | Drop mechanism |
| **Sensors** | | |
| IR Sensor | GPIO 41 | Object detection |
| **LEDs** | | |
| NeoPixel Ring | GPIO 1 | 16 LEDs for status indication |
| **Stepper Motor** | | |
| Stepper Motor | GPIO 2, 3, 4, 43 | Half-step motor control |
| **LCD Display** | | |
| I2C SDA | GPIO 5 | I2C data line |
| I2C SCL | GPIO 6 | I2C clock line |
| **Camera** | | |
| Camera | Default pins | OV2640 camera module |

> **Note**: All servos are connected to PWM channels with 50Hz frequency. The LCD display uses I2C address 0x27.

## 📋 Prerequisites

- MicroPython firmware
- Python 3.x
- ESP32 development board
- Required hardware components
- WiFi network access
- Google Gemini API key

## 🔧 Installation

1. **Flash MicroPython**:
   ```bash
   esptool.py --port /dev/ttyUSB0 erase_flash
   esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 micropython.bin
   ```

2. **Install Required Libraries**:
   ```python
   import upip
   upip.install('urequests')
   ```

3. **Configure WiFi Credentials**:
   Edit the following variables in `Garbage-Separator.py`:
   ```python
   SSID = 'your_wifi_ssid'
   PASSWORD = 'your_wifi_password'
   GEMINI_API_KEY = 'your_gemini_api_key'
   ```

## 🚀 Usage

1. Power on the device
2. Wait for WiFi connection (indicated by LCD display)
3. Place waste in the detection area
4. System will automatically:
   - Detect the waste
   - Capture an image
   - Classify the waste
   - Sort it into appropriate bin

## 📊 Waste Categories

- **Recyclable**: Plastics, paper, metal, glass
- **Non-recyclable**: Mixed materials, certain plastics
- **Organic**: Food waste, biodegradable materials

## 🔄 Project Structure

```
Garbage-IoT/
├── Garbage-Separator.py    # Main application code
├── neopixel_driver.py      # NeoPixel LED control
├── motor.py                # Stepper motor control
└── machine_i2c_lcd.py      # LCD display control
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for waste classification
- MicroPython community
- Open-source hardware community

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.

---

Made with ❤️ by [Your Name]