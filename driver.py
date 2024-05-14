import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException, NoSuchDriverException, SessionNotCreatedException,
    TimeoutException, JavascriptException)

from consts import SELECTOR_TYPES, DRIVER_SETTINGS
from tools.logger import logger


_log = logger.getLogger(__name__)


class Browser:
    _SELECTOR_METHODS = {
        SELECTOR_TYPES.XPATH: "_findElementByXpath",
        SELECTOR_TYPES.CSS: "_findElementByCss",
        SELECTOR_TYPES.TAG: "_findSubElementByTag"
    }

    def __init__(self, driverType):
        self.url = None
        self._settings = DRIVER_SETTINGS.getDriverByType(driverType)
        try:
            self._driver = self._settings.driver(service=self._settings.service, options=self._settings.options)
        except (NoSuchDriverException, SessionNotCreatedException):
            self._driver = self._settings.driver(options=self._settings.options)
        _log.debug(f"Created driver: {self._settings.driver}, {self._settings.options.arguments}")

    def openUrl(self, url):
        try:
            prevUrl = self.url
            self._driver.get(url)
            if self._driver.execute_script("return document.readyState") == "complete":
                self.url = url
                _log.debug(f"Open url: {url}")
                _log.debug(f"{prevUrl} -> {self.url}")
                return True
            return False
        except Exception as e:
            _log.error(f"Error occurred while opening page", exc_info=True)
            return False

    def findElement(self, selector, element=None, timeout=10, all=False):
        typeSelector = selector.type
        selectorName = selector.name
        selector = selector.selector
        _log.debug(f"Searching element using {typeSelector.name}: {selectorName}...")
        methodName = self._SELECTOR_METHODS.get(typeSelector)
        if methodName:
            method = getattr(self, methodName)
            return self._findElementWithRetry(method, selector, element, timeout, all)
        else:
            _log.error("Unsupported selector type")
            return None

    def _findElementWithRetry(self, method, selector, element, timeout, all):
        attempt = 0
        while attempt < 2:
            attempt += 1
            try:
                return method(selector, element, timeout, all)
            except (TimeoutException, NoSuchElementException, JavascriptException):
                _log.warning("Retrying...")
                continue
        _log.error("Maximum attempts reached. Element not found.")
        return None

    def _findElementByCss(self, css, element=None, timeout=10, all=False):
        if all:
            data = WebDriverWait(self._driver, timeout).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css))
            )
        else:
            data = WebDriverWait(self._driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css))
            )
        _log.debug("Element found using requested css")
        return data

    def _findElementByXpath(self, xpath, element=None, timeout=10, all=False):
        if all:
            data = WebDriverWait(self._driver, timeout).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )
        else:
            data = WebDriverWait(self._driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        return data

    def _findSubElementByTag(self, tag, element, timeout=10, all=False):
        if all:
            data = WebDriverWait(element, timeout).until(
                EC.visibility_of_all_elements_located((By.TAG_NAME, tag))
            )
        else:
            data = WebDriverWait(element, timeout).until(
                EC.visibility_of_element_located((By.TAG_NAME, tag))
            )
        return data

    def clickElement(self, element):
        try:
            beforeCountTabs = len(self.getTabs())
            element.click()
            time.sleep(1)

            afterCountTabs = len(self.getTabs())
            if beforeCountTabs < afterCountTabs:
                self.switchTab(self.getTabs()[-1])
            if self.isOnNewPage():
                _log.debug(f"{self.url} -> {self._driver.current_url}")
                self.url = self._driver.current_url
            return True
        except Exception:
            return False

    def isOnNewPage(self):
        if self.url != self._driver.current_url:
            return True
        else:
            return False

    def switchTab(self, tab):
        try:
            self._driver.switch_to.window(tab)
            return True
        except Exception:
            return False

    def getTabs(self):
        return self._driver.window_handles

    def close(self):
        self._driver.quit()
        self.url = None
        _log.debug("Close browser")

    @property
    def title(self):
        return self._driver.title

    @property
    def settings(self):
        return self._settings

    @property
    def driver(self):
        return self._driver
