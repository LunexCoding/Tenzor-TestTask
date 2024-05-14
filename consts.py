from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.firefox.service import Service as firefoxService

from settingsConfig import g_settingsConfig


DRIVER = namedtuple("DRIVER", ["type", "service", "options", "driver"])


class DRIVER_TYPES:
    CHROME = 0
    FIREFOX = 1


OPTIONS = ["--headless"]
CHROME_OPTIONS = webdriver.ChromeOptions()
FIREFOX_OPTIONS = webdriver.FirefoxOptions()
for option in OPTIONS:
    CHROME_OPTIONS.add_argument(option)
    FIREFOX_OPTIONS.add_argument(option)


class DRIVER_SETTINGS:
    CHROME = DRIVER(
        DRIVER_TYPES.CHROME,
        chromeService(executable_path=g_settingsConfig.DriversSettings["chrome"]),
        CHROME_OPTIONS,
        webdriver.Chrome
    )
    FIREFOX = DRIVER(
        DRIVER_TYPES.FIREFOX,
        firefoxService(executable_path=g_settingsConfig.DriversSettings["firefox"]),
        FIREFOX_OPTIONS,
        webdriver.Firefox
    )

    @classmethod
    def getDriverByType(cls, driver_type):
        for driverSetting in cls.__dict__.values():
            if isinstance(driverSetting, DRIVER) and driverSetting.type == driver_type:
                return driverSetting
        return None


SELECTOR_TYPE = namedtuple("SELECTOR_TYPE", ["id", "name"])


class SELECTOR_TYPES:
    XPATH = SELECTOR_TYPE(0, "xpaths")
    CSS = SELECTOR_TYPE(1, "css")
    TAG = SELECTOR_TYPE(2, "tag")


SELECTOR = namedtuple("SELECTOR", ["name", "type", "selector"])


class Constants:
    MY_REGION = "Новосибирская обл."
    REQUIRED_REGION = "Камчатский край"


class SELECTORS:
    CONTACTS = SELECTOR("CONTACTS", SELECTOR_TYPES.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/a[1]")
    LOGO = SELECTOR("LOGO", SELECTOR_TYPES.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]")
    BLOCK_POWER_IN_PEOPLE = SELECTOR("BLOCK_POWER_IN_PEOPLE", SELECTOR_TYPES.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]")
    WORKING_SECTION = SELECTOR("WORKING_SECTION", SELECTOR_TYPES.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]")
    WORKING_SECTION_IMAGE = SELECTOR("WORKING_SECTION_IMAGE", SELECTOR_TYPES.XPATH, "//body/div[@id='wasaby-content']/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[2]/div[2]/a[1]/div[1]/div[1]")
    REGION = SELECTOR("REGION", SELECTOR_TYPES.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/span[1]/span[1]")
    REQUIRED_REGION = SELECTOR("REQUIRED_REGION", SELECTOR_TYPES.XPATH, f"//span[contains(text(),'{Constants.REQUIRED_REGION}')]")
    PARTNER_CITY = SELECTOR("PARTNER_CITY", SELECTOR_TYPES.XPATH, "//div[@id='city-id-{}']")
    PARTNER_BLOCK = SELECTOR("PARTNER_BLOCK", SELECTOR_TYPES.XPATH, "//body/div[@id='wasaby-content']/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[{}]")
    PARTNER_SHORT_INFO = SELECTOR("PARTNER_SHORT_INFO", SELECTOR_TYPES.XPATH, "//body/div[@id='wasaby-content']/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[{}]/div[1]/div[1]/div[1]")
    PARTNER_PHONE = SELECTOR("PARTNER_PHONE", SELECTOR_TYPES.XPATH, "//body/div[@id='wasaby-content']/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[{}]/div[1]/div[1]/div[2]")
    PARTNER_ADDITIONAL_CONTACTS = SELECTOR("PARTNER_ADDITIONAL_CONTACTS", SELECTOR_TYPES.XPATH, "//body/div[@id='wasaby-content']/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[{}]/div[1]/div[1]/div[3]")
    IMG = SELECTOR("IMG", SELECTOR_TYPES.TAG, "img")
    LINK = SELECTOR("LINK", SELECTOR_TYPES.TAG, "a")
