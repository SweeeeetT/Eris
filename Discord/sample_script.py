import discord

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

"""CONFIGURATION SETTINGS"""
DEBUGGING = True
TIMEOUT = 10

class DiscordCreds:
    """Stores Discord login credentials"""
    def __init__(self):
        self.login = "" #user email
        self.password = "" #user password

class DiscreetBot():
    """Webdriver Configuration for discord test"""
    def __init__(self):
        """Options for Chrome"""
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications" : 2})
        if not DEBUGGING:
            chrome_options.add_argument("--headless")
        self.creds = DiscordCreds()
        self.driver = webdriver.Chrome(options=chrome_options)

def discord_login(bot):
    """Logs in to discord"""
    bot.driver.get("https://discord.com/login")
    WebDriverWait(bot.driver, TIMEOUT)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR,  "[name='email']")))
    bot.driver.find_element(By.CSS_SELECTOR, "[name='email']").send_keys(bot.creds.login)
    bot.driver.find_element(By.CSS_SELECTOR, "[aria-label='Password']").send_keys(bot.creds.password)
    bot.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

def main():
    bot = DiscreetBot()
    discord_login(bot)
    config = discord.DiscordConfiguration(TIMEOUT)
    home = discord.DiscordHome(bot.driver, config)

    #Perform needed actions

    #Hang for debugging
    if DEBUGGING:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("[+] Exiting")

    bot.driver.quit()

if __name__ == "__main__":
    main()
