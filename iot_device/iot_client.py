import network
import time
import urequests
import ure as re
from machine import Pin, I2C
import ssd1306

CONFIG = {
    "SSID": "Wokwi-GUEST",
    "PASSWORD": "",
    "SERVER_URL": "https://late-baboons-hide.loca.lt", 
    "DEVICE_ID": 4,
    "SCAN_DELAY": 5 
}

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def display_message(l1, l2="", l3=""):
    oled.fill(0)
    oled.text(l1, 0, 0)
    oled.text(l2, 0, 20)
    oled.text(l3, 0, 40)
    oled.show()

def validate_and_format_url(qr_data):
    if len(qr_data) == 36 and qr_data.count('-') == 4:
        base_url = CONFIG['SERVER_URL']
        dev_id = CONFIG['DEVICE_ID']
        return "{}/scan/{}?user_id={}".format(base_url, qr_data, dev_id)
    return None

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...", end="")
        wlan.connect(CONFIG["SSID"], CONFIG["PASSWORD"])
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
    print("\n[OK] IP:", wlan.ifconfig()[0])
    display_message("LumiCosm", "WiFi Connected", wlan.ifconfig()[0])
    time.sleep(1)

def start_iot_client():
    connect_wifi()
    test_qr = "9b4b574d-daa6-41b9-90d4-0e418284f639" 
    
    while True:
        print(f"\n[SCAN] Обробка нового зчитування...")
        request_url = validate_and_format_url(test_qr)        
        if request_url:
            print(f"[DEBUG] Сформовано URL: {request_url}")
            display_message("Scanning...", "Connecting API")           
            try:
                headers = {
                    "ngrok-skip-browser-warning": "true",
                    "User-Agent": "ESP32_LumiCosm_Client",
                    "Connection": "close"
                }            
                res = urequests.get(request_url, headers=headers, timeout=10)
                
                print(f"[HTTP] Статус: {res.status_code}")
                
                if res.status_code == 200:
                    response_data = res.json()
                    status = response_data.get('status_calculated', 'OK')
                    prod = response_data.get('product_name', 'Item')
                    
                    print(f"[SUCCESS] {prod}: {status}")
                    display_message("MATCH!", prod[:15], status)
                else:
                    print(f"[SERVER ERROR] Код: {res.status_code}")
                    display_message("Err Code:", str(res.status_code))
                
                res.close() 

            except Exception as e:
                print(f"[FAIL] Помилка з'єднання: {e}")
                display_message("Conn. Error", "Check Link")
        else:
            print("[FAIL] Некоректний формат даних")
            display_message("Data Error", "Invalid UUID")
        
        print(f"Очікування {CONFIG['SCAN_DELAY']} сек...")
        time.sleep(CONFIG["SCAN_DELAY"])

if __name__ == "__main__":
    start_iot_client()