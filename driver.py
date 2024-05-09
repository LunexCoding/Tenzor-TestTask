from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchDriverException, SessionNotCreatedException

from consts import SELECTORS, SELECTOR_TYPES, DRIVER_SETTINGS
from tools.logger import logger


_log = logger.getLogger(__name__)


class Browser:
    _SELECTOR_METHODS = {
        SELECTOR_TYPES.XPATH: "_findElementByXpath",
        SELECTOR_TYPES.CSS: "_findElementByCss"
    }

    def __init__(self, driverType):
        self._url = None
        self._settings = DRIVER_SETTINGS.getDriverByType(driverType)
        try:
            self._driver = self._settings.driver(service=self._settings.service, options=self._settings.options)
        except (NoSuchDriverException, SessionNotCreatedException):
            self._driver = self._settings.driver(options=self._settings.options)
        _log.debug(f"Created driver: {self._settings.driver}, {self._settings.options.arguments}")

    def openUrl(self, url):
        try:
            prevUrl = self._url
            self._driver.get(url)
            if self._driver.execute_script("return document.readyState") == "complete":
                self._url = url
                _log.debug(f"Open url: {url}")
                _log.debug(f"{prevUrl} -> {self._url}")
                return True
        except Exception as e:
            _log.error(f"Error occurred while opening page: {e}")
            return False

    def findElement(self, element, timeout=10, all=False):
        typeSelector = element.type
        selector = element.selector
        _log.debug(f"Searching element using {typeSelector.name}: {SELECTORS.getElementName(selector)}...")
        methodName = self._SELECTOR_METHODS.get(typeSelector)
        if methodName:
            method = getattr(self, methodName)
            return method(selector, timeout, all)
        else:
            _log.error("Unsupported selector type")
            return None

    def _findElementByCss(self, css, timeout=10, all=False):
        try:
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
        except NoSuchElementException:
            _log.error("Element not found using requested css")
            return None

    def _findElementByXpath(self, xpath, timeout=10, all=False):
        try:
            if all:
                data = WebDriverWait(self._driver, timeout).until(
                    EC.visibility_of_all_elements_located((By.XPATH, xpath))
                )
            else:
                data = WebDriverWait(self._driver, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
            _log.debug("Element found using requested Xpath")
            return data
        except NoSuchElementException:
            _log.error("Element not found using requested Xpath")
            return None

    def clickElement(self, element):
        try:
            element.click()
            if self.isOnNewPage():
                _log.debug(f"{self._url} -> {self._driver.current_url}")
                self._url = self._driver.current_url
                return True
        except Exception:
            return False

    @staticmethod
    def findSubElementByTag(element, tag, timeout=10, all=False):
        _log.debug(f"Searching sub element by tag: {tag}...")
        try:
            if all:
                data = WebDriverWait(element, timeout).until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, tag))
                )
            else:
                data = WebDriverWait(element, timeout).until(
                    EC.visibility_of_element_located((By.TAG_NAME, tag))
                )
            _log.debug("Sub element found using requested tag")
            return data
        except NoSuchElementException:
            _log.error(f"Sub element with tag '{tag}' not found")
            return None

    def isOnNewPage(self):
        if self._url != self._driver.current_url:
            return True
        else:
            return False

    def close(self):
        self._driver.quit()
        _log.debug("Close browser")
