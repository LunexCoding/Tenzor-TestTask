from actions import *
from scenario import Scenario
from tools.logger import logger
from consts import Constants, DRIVER_TYPES


_log = logger.getLogger(__name__)


if __name__ == "__main__":
    scenarioFirst = Scenario(DRIVER_TYPES.CHROME, "Сценарий 1")
    scenarioFirst.addAction(OpenStartPageAction, "https://sbis.ru/"),
    scenarioFirst.addAction(ClickContactsAction),
    scenarioFirst.addAction(OpenLogoLinkAction),
    scenarioFirst.addAction(OpenAboutPageAction),
    scenarioFirst.addAction(ComparisonPicturesWorkingSectionAction)
    scenarioFirst.perform()

    scenarioSecond = Scenario(DRIVER_TYPES.CHROME, "Сценарий 2")
    scenarioSecond.addAction(OpenStartPageAction, "https://sbis.ru/"),
    scenarioSecond.addAction(ClickContactsAction),
    scenarioSecond.addAction(FindRegionElementAction),
    scenarioSecond.addAction(VerifyRegionAction, Constants.MY_REGION),
    scenarioSecond.addAction(GetPartnersAction, "dataBeforeChange"),
    scenarioSecond.addAction(ChangeRegionAction),
    scenarioSecond.addAction(FindRegionElementAction),
    scenarioSecond.addAction(VerifyRegionAction, Constants.REQUIRED_REGION),
    scenarioSecond.addAction(GetPartnersAction, "dataAfterChange"),
    scenarioSecond.addAction(CompareDataAction, scenarioSecond, ["dataBeforeChange", "dataAfterChange"])
    scenarioSecond.perform()
