from consts import SELECTORS
from tools.logger import logger


__all__ = ["OpenHomePageAction", "ClickBannerAction", "OpenLogoLinkAction", "OpenAboutPageAction", "ComparisonPicturesWorkingSectionAction"]

_log = logger.getLogger(__name__)


class Action:
    def __init__(self, browser):
        self.browser = browser

    def execute(self):
        pass


class OpenHomePageAction(Action):
    def execute(self):
        max_attempts = 3
        current_attempt = 1

        while current_attempt <= max_attempts:
            if not self.browser.openUrl("https://sbis.ru/"):
                _log.error("Failed to open home page, retrying...")
                current_attempt += 1
            else:
                return True

        _log.error("Failed to open home page after multiple attempts")
        return False


class ClickBannerAction(Action):
    def execute(self):
        banner = self.browser.findElement(SELECTORS.BANNER)
        if not banner:
            return False

        self.browser.clickElement(banner)
        return True


class OpenLogoLinkAction(Action):
    def execute(self):
        logo = self.browser.findElement(SELECTORS.LOGO)
        if not logo:
            return False

        link = logo.get_attribute("href")
        if not link:
            return False

        return self.browser.openUrl(link)


class OpenAboutPageAction(Action):
    def execute(self):
        block = self.browser.findElement(SELECTORS.BLOCK_POWER_IN_PEOPLE)
        if not block:
            return False

        link_element = self.browser.findSubElementByTag(block, "a")
        if not link_element:
            return False

        link = link_element.get_attribute("href")
        if not link:
            return False

        return self.browser.openUrl(link)


class ComparisonPicturesWorkingSectionAction(Action):
    def execute(self):
        section = self.browser.findElement(SELECTORS.WORKING_SECTION)
        if not section:
            return False

        images = self.browser.findSubElementByTag(section, "img", all=True)
        if not images:
            return False

        alts = [image.get_attribute("alt") for image in images]
        if all(alt == alts[0] for alt in alts):
            return False

        widths = [int(image.get_attribute("width")) for image in images]
        heights = [int(image.get_attribute("height")) for image in images]
        if not (widths and heights):
            return False

        sizes = list(zip(widths, heights))
        if not all(size == sizes[0] for size in sizes):
            return False

        return True
