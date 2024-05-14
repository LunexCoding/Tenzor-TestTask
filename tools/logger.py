from pathlib import Path

from Logger import Logger
from settingsConfig import g_settingsConfig


logger = Logger()
logger.createLog(g_settingsConfig.LogSettings["directory"], g_settingsConfig.LogSettings["file"])
with open(Path(g_settingsConfig.LogSettings["directory"], g_settingsConfig.LogSettings["file"]), "w") as file:
    file.write('```python\n')
