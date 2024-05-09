from tools.logger import logger


_log = logger.getLogger(__name__)


class Scenario:
    def __init__(self, browser, name):
        self._browser = browser
        self._name = name
        self.actions = []

    def addAction(self, action):
        self.actions.append(action)

    def perform(self):
        _log.debug(f"Scenario {self.name} running")
        try:
            for action in self.actions:
                if not action.execute():
                    _log.error(f"Action {action.__class__} failed")
                    _log.debug(f"Scenario {self.name} failed")
                    return False
            _log.debug(f"Scenario {self.name} performed")
            return True
        except Exception as e:
            _log.error(f"Error. {e}")
            _log.debug(f"Scenario {self.name} failed")
            return False
        finally:
            self._browser.close()

    @property
    def browser(self):
        return self._browser

    @property
    def name(self):
        return self._name
