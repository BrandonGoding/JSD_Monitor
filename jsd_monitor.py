import time
import requests
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configuration
JSD60_URL = f"http://{config('LOCAL_IP')}"
CGI_URL = f"{JSD60_URL}/dynamic.cgi"
EXPECTED_BUTTON_NUM = "2"
MINIMUM_FADER_LEVEL = 38


def get_jsd_status():
    """Fetch current ButtonNum and Fader value from dynamic.cgi"""
    response = requests.get(CGI_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch CGI: {response.status_code}")

    parts = response.text.split(";")
    data = {}
    for part in parts:
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            data[key] = value

    return {
        "ButtonNum": data.get("ButtonNum", None),
        "CurrentFader": float(data.get("CurrentFader", 0.0))
    }

def click_button2_with_selenium():
    """Use Selenium to click the Button 2 (Digital 8) input selector"""
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(JSD60_URL)
        time.sleep(1)

        # Wait for button2 to appear and click it
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "button2"))
        )

        print("🔘 Clicking button2...")
        button.click()

    finally:
        driver.quit()

def increase_volume_with_selenium(current_fader, target_fader=3.9):
    """Click 'Fader Up' the number of times needed to reach the target level."""
    steps_needed = int(target_fader - current_fader)

    if steps_needed <= 0:
        print("✅ Volume already at or above target.")
        return

    print(f"🔊 Need to increase volume by {steps_needed * 0.10:.2f} — {steps_needed} clicks")

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(JSD60_URL)
        time.sleep(1)

        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@onclick='FaderRel(+10)']"))
        )

        for i in range(steps_needed):
            print(f"🔼 Click {i+1}/{steps_needed}")
            button.click()
            time.sleep(0.3)  # Small delay between clicks

    finally:
        driver.quit()


def main():
    status = get_jsd_status()
    button_num = status["ButtonNum"]
    current_fader = status["CurrentFader"]

    print(f"🎯 Current ButtonNum: {button_num}")
    print(f"🎚️  CurrentFader: {current_fader:.2f}")

    # Step 1: Switch channel if needed
    if button_num != EXPECTED_BUTTON_NUM:
        print("⚠️ Not on Button 2 — correcting it with Selenium...")
        click_button2_with_selenium()

        # 🔁 Re-fetch status after switching channel
        time.sleep(5)  # optional wait to let state update
        status = get_jsd_status()
        current_fader = status["CurrentFader"]
        print(f"🔄 Re-fetched CurrentFader: {current_fader:.2f}")
    else:
        print("✅ Already on Button 2 — no action needed.")

    # Step 2: Check fader and increase if needed
    if current_fader < MINIMUM_FADER_LEVEL:
        increase_volume_with_selenium(current_fader, MINIMUM_FADER_LEVEL)
    else:
        print("✅ Fader is at or above minimum level — no action needed.")


if __name__ == "__main__":
    main()
