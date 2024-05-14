from tools.logger import logger
from driver import Browser


_log = logger.getLogger(__name__)


class Scenario:
    def __init__(self, browserType, name):
        self._browser = Browser(browserType)
        self._name = name
        self.actions = []
        self.slots = {}

    def addAction(self, action, *args, **kwargs):
        actionInstance = action(*args, **kwargs)
        self.actions.append(actionInstance)

    def perform(self):
        _log.debug(f"Scenario {self._name} running")
        try:
            for action in self.actions:
                inputData = self.getInput(action)
                outputData = action.execute(self._browser, inputData)
                self.setOutput(action, outputData)
                if not outputData or 'success' not in outputData or not outputData['success']:
                    _log.error(f"Action {action.__class__} failed")
                    _log.debug(f"Scenario {self._name} failed")
                    return False
            _log.debug(f"Scenario {self._name} performed")
            return True
        except Exception as e:
            _log.error(f"Error. {e}", exc_info=True)
            _log.debug(f"Scenario {self._name} failed")
            return False
        finally:
            self._browser.close()

    def getInput(self, action):
        inputSlots = getattr(action, 'inputSlots', [])
        inputData = {}
        for slotName in inputSlots:
            inputData[slotName] = self.slots.get(slotName)
        return inputData

    def setOutput(self, action, output_data):
        outputSlots = getattr(action, 'outputSlots', [])
        for slotName in outputSlots:
            self.slots[slotName] = output_data.get(slotName)

    def initializeSlots(self, slotNames):
        for slotName in slotNames:
            self.slots[slotName] = None

    @property
    def name(self):
        return self._name
