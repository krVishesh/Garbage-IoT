import machine
import time
import network
import camera
import urequests
import ubinascii
import gc
from machine import Pin, SoftI2C
from neopixel_driver import NeoPixel  # Save your driver as 'neopixel_driver.py'
from motor import HalfStepMotor  # Import the HalfStepMotor class from motor.py'
from machine_i2c_lcd import I2cLcd

# Define pins
SERVO1_PIN_FRONT = 9
SERVO2_PIN_FRONT = 8
IR_SENSOR_PIN = 41
SERVO1_PIN_DROP = 7
SERVO2_PIN_DROP = 44
NEOPIXEL_PIN = 1
NUM_PIXELS = 16
STEPPER_PINS = [2, 3, 4, 43]
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

# Initialize devices
servo_front_1 = machine.PWM(machine.Pin(SERVO1_PIN_FRONT), freq=50)
servo_front_2 = machine.PWM(machine.Pin(SERVO2_PIN_FRONT), freq=50)
servo_drop_1 = machine.PWM(machine.Pin(SERVO1_PIN_DROP), freq=50)
servo_drop_2 = machine.PWM(machine.Pin(SERVO2_PIN_DROP), freq=50)
ir_sensor = machine.Pin(IR_SENSOR_PIN, machine.Pin.IN)
np = NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)
stepper = HalfStepMotor.frompins(*STEPPER_PINS)

i2c = SoftI2C(sda=Pin(5), scl=Pin(6), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Wi-Fi Credentials
SSID = '...'
PASSWORD = '...'
GEMINI_API_KEY = '...'
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}'

# Connect to Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
    print('Connected!')

connect_to_wifi(SSID, PASSWORD)

cam = camera.init()
# Set Camera Preferences
camera.framesize(8)     # Frame size 800x600 (1.33 aspect ratio)
camera.contrast(2)      # Increase contrast
camera.speffect(0)      # Apply grayscale effect
camera.brightness(1)    # Increase Brightness
camera.quality(10)      # Quality to Max (lower is better) 10 - 63

lcd.clear()
lcd.putstr("Ready")

def set_servos_angle(servo1, servo2, angle1, angle2):
    duty1 = int(20 + (angle1 / 180) * 100)
    duty2 = int(20 + (angle2 / 180) * 100)
    servo1.duty(duty1)
    servo2.duty(duty2)

def neopixel_fill(color):
    np.fill(color)
    np.write()
    time.sleep(1)

def capture_photo():
    print("Capturing photo...")
    img = camera.capture()
    if img:
        with open("photo.jpg", "wb") as f:
            f.write(img)
        print("Photo captured successfully!")
        return "photo.jpg"
    print("Failed to capture photo.")
    return None

def detect_waste(photo_path):
    print("Processing image for waste detection...")
    with open(photo_path, 'rb') as f:
        encoded_img = ubinascii.b2a_base64(f.read()).decode('utf-8').replace("\n", "")
        data = {"contents": [{"parts": [{"text": "Categorise the waste material in this image into Recyclable, Non-recyclable, Organic. Answer only in these 3 categories and Single Word."}, {"inline_data": {"mime_type": "image/jpeg", "data": encoded_img}}]}]}
        response = urequests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, json=data)
        print("Response received from API.")
        if response.status_code == 200:
            category = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Unknown")
            print(f"Detected waste category: {category}")
            return category
    print("Failed to detect waste category.")
    return "Unknown"

try:
    while True:
        if ir_sensor.value() == 0:
            lcd.clear()
            lcd.putstr("Processing...")
            print("Object detected by IR sensor.")
            set_servos_angle(servo_front_1, servo_front_2, 135, 49)
            time.sleep(3)
            set_servos_angle(servo_front_1, servo_front_2, 4, 180)
            time.sleep(2)
            neopixel_fill((255, 255, 255))
            photo = capture_photo()
            if photo:
                category = detect_waste(photo)
                lcd.clear()
                lcd.putstr(f"Category: {category}")
                time.sleep(2)
                if category == "Recyclable":
                    print("Moving stepper for Recyclable waste.")
                    stepper.step(600)
                elif category == "Non-recyclable":
                    print("Moving stepper for Non-recyclable waste.")
                    stepper.step(-600)
                time.sleep(2)
                set_servos_angle(servo_drop_1, servo_drop_2, 70, 70)
                time.sleep(3)
                set_servos_angle(servo_drop_1, servo_drop_2, 4, 4)
                time.sleep(3)
                if category in ["Recyclable", "Non-recyclable"]:
                    print("Returning stepper to original position.")
                    stepper.step(-600 if category == "Recyclable" else 600)
            lcd.clear()
            neopixel_fill((0, 0, 0))
            lcd.putstr("Ready")
except KeyboardInterrupt:
    servo_front_1.deinit()
    servo_front_2.deinit()
    servo_drop_1.deinit()
    servo_drop_2.deinit()
    print("Stopped script.")

