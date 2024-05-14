import pytest

from consts import DRIVER_TYPES, DRIVER_SETTINGS, SELECTOR, SELECTOR_TYPES
from driver import Browser


class TestDriver:

    @pytest.fixture
    def openUrl(self):
        return "https://sbis.ru/"

    @pytest.fixture
    def xpathSelector(self):
        return SELECTOR("Google button", SELECTOR_TYPES.XPATH, "//body/div[@id='wasaby-content']/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[2]/a[1]")

    def test_driverChrome(self):
        driver = Browser(DRIVER_TYPES.CHROME)
        assert driver.settings.type == DRIVER_TYPES.CHROME
        assert driver.settings.service == DRIVER_SETTINGS.CHROME.service
        assert driver.settings.options == DRIVER_SETTINGS.CHROME.options
        assert driver.settings.driver == DRIVER_SETTINGS.CHROME.driver
        driver.close()

    def test_driverFirefox(self):
        driver = Browser(DRIVER_TYPES.FIREFOX)
        assert driver.settings.type == DRIVER_TYPES.FIREFOX
        assert driver.settings.service == DRIVER_SETTINGS.FIREFOX.service
        assert driver.settings.options == DRIVER_SETTINGS.FIREFOX.options
        assert driver.settings.driver == DRIVER_SETTINGS.FIREFOX.driver
        driver.close()

    def test_openUrl(self, openUrl):
        driver = Browser(DRIVER_TYPES.CHROME)
        assert driver.openUrl(openUrl)
        assert driver.url == openUrl
        driver.close()

    def test_switchTab(self):
        driver = Browser(DRIVER_TYPES.CHROME)
        driver.openUrl(self.openUrl)
        driver.driver.execute_script("window.open('');")
        assert len(driver.getTabs()) == 2
        assert driver.switchTab(driver.getTabs()[-1])
        assert driver.isOnNewPage()
        driver.close()

    def test_findElement(self, openUrl, xpathSelector):
        driver = Browser(DRIVER_TYPES.CHROME)
        driver.openUrl(openUrl)
        assert driver.findElement(xpathSelector) is not None
        driver.close()

    def test_findElementAll(self, openUrl, xpathSelector):
        driver = Browser(DRIVER_TYPES.CHROME)
        driver.openUrl(openUrl)
        element = driver.findElement(xpathSelector, all=True)
        assert element is not None
        assert isinstance(element, list)
        assert element
        driver.close()

    def test_clickElement(self, openUrl, xpathSelector):
        driver = Browser(DRIVER_TYPES.CHROME)
        driver.openUrl(openUrl)
        element = driver.findElement(xpathSelector)
        assert element is not None
        assert driver.clickElement(element)
        driver.close()
