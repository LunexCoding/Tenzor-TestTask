from actions import *
from driver import Browser

from scenario import Scenario
from tools.logger import logger
from consts import DRIVER_TYPES


_log = logger.getLogger(__name__)


if __name__ == "__main__":
    browser = Browser(DRIVER_TYPES.CHROME)

    scenario = Scenario(browser, "Сценарий 1")
    scenario.addAction(OpenHomePageAction(browser))
    scenario.addAction(ClickBannerAction(browser))
    scenario.addAction(OpenLogoLinkAction(browser))
    scenario.addAction(OpenAboutPageAction(browser))
    scenario.addAction(ComparisonPicturesWorkingSectionAction(browser))
    scenario.perform()
