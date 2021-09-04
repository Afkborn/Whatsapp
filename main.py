from Python.Whatsapp import Whatsapp # Import Whatsapp Class

from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx
import shutil
import platform
from os import listdir

VERLIST = ['93.','92.','91.']





def getDefaultBrowser():
    browser_path = shutil.which('open')
    osPlatform = platform.system()
    if osPlatform == 'Windows':
        try:
            with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as regkey:
                browser_choice = QueryValueEx(regkey, 'ProgId')[0]
            with OpenKey(HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(browser_choice)) as regkey:
                browser_path_tuple = QueryValueEx(regkey, None)
                browser_path = browser_path_tuple[0].split('"')[1]
                
                global CHROMEVERSION
                if "chrome" in browser_path:
                    browserLoc = browser_path.replace('\chrome.exe',"")
                    
                    for folderName in listdir(browserLoc):
                        for ver in VERLIST:
                            if ver in folderName :
                                CHROMEVERSION = folderName
                    return True
                else:
                    print("set default browser chrome")
                    return False
        except Exception:
            return False
    return False



if __name__ == "__main__":
    if getDefaultBrowser():
        print("ok")

