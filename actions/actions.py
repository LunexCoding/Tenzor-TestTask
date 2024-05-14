from consts import SELECTORS, SELECTOR
from tools.logger import logger


_log = logger.getLogger(__name__)


class Action:
    def __init__(self, dynamicOutputSlots=None):
        self.outputSlots = ['success']
        if dynamicOutputSlots:
            self.addDynamicOutputSlots(dynamicOutputSlots)

    def addDynamicOutputSlots(self, dynamicOutputSlots):
        if isinstance(dynamicOutputSlots, list):
            self.outputSlots.extend(dynamicOutputSlots)
        else:
            self.outputSlots.append(dynamicOutputSlots)

    def execute(self, browser, inputData):
        pass


class OpenStartPageAction(Action):
    def __init__(self, startPageUrl):
        super().__init__()
        self._startPageUrl = startPageUrl

    def execute(self, browser, inputData):
        if not self._startPageUrl:
            return {'success': False}

        maxAttempts = 3
        currentAttempt = 1

        while currentAttempt <= maxAttempts:
            if not browser.openUrl(self._startPageUrl):
                _log.error("Failed to open home page, retrying...")
                currentAttempt += 1
            else:
                return {'success': True}
        _log.error("Failed to open home page after multiple attempts")
        return {'success': False}


class ClickContactsAction(Action):
    def __init__(self):
        super().__init__()

    def execute(self, browser, inputData):
        contacts = browser.findElement(SELECTORS.CONTACTS)
        if not contacts:
            return {'success': False}

        if not browser.clickElement(contacts):
            return {'success': False}

        return {'success': True}


class OpenLogoLinkAction(Action):
    def __init__(self):
        super().__init__()

    def execute(self, browser, inputData):
        logo = browser.findElement(SELECTORS.LOGO)
        if not logo:
            return {'success': False}

        if not browser.clickElement(logo):
            return {'success': False}

        return {'success': True}


class OpenAboutPageAction(Action):
    def __init__(self):
        super().__init__()

    def execute(self, browser, inputData):
        block = browser.findElement(SELECTORS.BLOCK_POWER_IN_PEOPLE)
        if not block:
            return {'success': False}

        linkElement = browser.findElement(SELECTORS.LINK, block)
        if not linkElement:
            return {'success': False}

        link = linkElement.get_attribute("href")
        if not link:
            return {'success': False}

        if not browser.openUrl(link):
            return {'success': False}

        return {'success': True}


class ComparisonPicturesWorkingSectionAction(Action):
    def __init__(self):
        super().__init__()

    def execute(self, browser, inputData):
        section = browser.findElement(SELECTORS.WORKING_SECTION)
        if not section:
            return {'success': False}

        images = browser.findElement(SELECTORS.IMG, section, all=True)
        if not images:
            return {'success': False}

        alts = [image.get_attribute("alt") for image in images]
        if all(alt == alts[0] for alt in alts):
            return {'success': False}

        widths = [int(image.get_attribute("width")) for image in images]
        heights = [int(image.get_attribute("height")) for image in images]
        if not (widths and heights):
            return {'success': False}

        sizes = list(zip(widths, heights))
        if not all(size == sizes[0] for size in sizes):
            return {'success': False}

        return {'success': True}


class FindRegionElementAction(Action):
    def __init__(self):
        super().__init__()
        self.addDynamicOutputSlots("region")

    def execute(self, browser, inputData):
        region = browser.findElement(SELECTORS.REGION)
        if region is None:
            return {'success': False, 'region': region}

        return {'success': True, 'region': region}


class VerifyRegionAction(Action):
    inputSlots = ['region']

    def __init__(self, requiredRegion):
        super().__init__()
        self._requiredRegion = requiredRegion

    def execute(self, browser, inputData):
        region = inputData.get('region')
        if region is None:
            return {'success': False}

        if not region.text == self._requiredRegion:
            return {'success': False}

        return {'success': True}


class ChangeRegionAction(Action):
    inputSlots = ['region']

    def execute(self, browser, inputData):
        region = inputData.get('region')
        if region is None:
            return {'success': False}

        if not browser.clickElement(region):
            return {'success': False}

        requiredRegionElement = browser.findElement(SELECTORS.REQUIRED_REGION)
        if not requiredRegionElement:
            return {'success': False}

        if not browser.clickElement(requiredRegionElement):
            return {'success': False}

        return {'success': True}


class GetPartnersAction(Action):
    def __init__(self, slotName):
        super().__init__(dynamicOutputSlots=slotName)
        self._slotName = slotName

    def execute(self, browser, inputData):
        sityCount = 2
        count = 2
        partners = {}

        sity = self._findSity(browser, sityCount)
        partners[sity] = []

        while True:
            try:
                partnerBlock = self._findPartnerBlock(browser, count)
                if partnerBlock is None:
                    break

                shortInfo = self._findShortInfo(browser, count)
                name = shortInfo.pop(0)
                phone = self._findPhone(browser, count)
                email, site = self._findAdditionalContacts(browser, count)

                partner = {
                    "name": name,
                    "address": shortInfo,
                    "phone": phone,
                    "email": email,
                    "site": site
                }
                partners[sity].append(partner)
                count += 1
            except Exception:
                sityCount += 1
                count += 1
                sity = self._findSity(browser, sityCount)
                partners[sity] = []

        return {'success': True, self._slotName: partners}

    def _findSity(self, browser, sityCount):
        sitySelector = SELECTOR(SELECTORS.PARTNER_CITY.name, SELECTORS.PARTNER_CITY.type, SELECTORS.PARTNER_CITY.selector.format(sityCount))
        sity = browser.findElement(sitySelector).text
        return sity

    def _findPartnerBlock(self, browser, count):
        partnerBlockSelector = SELECTOR(SELECTORS.PARTNER_BLOCK.name, SELECTORS.PARTNER_BLOCK.type, SELECTORS.PARTNER_BLOCK.selector.format(count))
        partnerBlock = browser.findElement(partnerBlockSelector)
        return partnerBlock

    def _findShortInfo(self, browser, count):
        shortInfoSelector = SELECTOR(SELECTORS.PARTNER_SHORT_INFO.name, SELECTORS.PARTNER_SHORT_INFO.type, SELECTORS.PARTNER_SHORT_INFO.selector.format(count))
        shortInfo = browser.findElement(shortInfoSelector).text.split("\n")
        return shortInfo

    def _findPhone(self, browser, count):
        phoneSelector = SELECTOR(SELECTORS.PARTNER_PHONE.name, SELECTORS.PARTNER_PHONE.type, SELECTORS.PARTNER_PHONE.selector.format(count))
        phone = browser.findElement(phoneSelector).text.split("\n")
        return phone

    def _findAdditionalContacts(self, browser, count):
        email = []
        site = []
        additionalContactsSelector = SELECTOR(SELECTORS.PARTNER_ADDITIONAL_CONTACTS.name, SELECTORS.PARTNER_ADDITIONAL_CONTACTS.type, SELECTORS.PARTNER_ADDITIONAL_CONTACTS.selector.format(count))
        contacts = browser.findElement(additionalContactsSelector).text.split("\n")
        for contact in contacts:
            if "@" in contact:
                email.append(contact)
            else:
                site.append(contact)
        return email, site


class CompareDataAction(Action):
    def __init__(self, scenario, slotName):
        super().__init__()
        self._scenario = scenario
        self._slotNames = slotName

    def execute(self, browser, inputData):
        data = []
        for slotName in self._slotNames:
            data.append(self._scenario.slots.get(slotName))

        if all(element == data[0] for element in data):
            return {'success': False}

        return {'success': True}
