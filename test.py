import os
import shutil

configDirectoryPath = "{}/.config/os-setup".format(os.getenv("HOME"))
configFilePath = configDirectoryPath + "/config-targets.conf"
configBackupPath = "{}/.os-setup-configs-backup".format(os.getenv("HOME"))

cacheBasePath = "{}/.cache".format(os.getenv("HOME"))
cacheDirectoryPath = cacheBasePath + "/os-setup"
# This is a .conf file that serves as a cache to compare and contrast
# for updates in comparison to the primary .conf file. 
cacheFilePath = cacheDirectoryPath + "/config-targets-cache.conf" 

shutil.copy(configFilePath, cacheFilePath)