from os import getcwd
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep 
class Whatsapp: 
    __chromeDriverPath = getcwd() +  fr"/Driver/chromedriver.exe"
    __whatsappURL = "https://web.whatsapp.com/"
    def __init__(self,chromeVer,profileName,headless = False) -> None:
        self.__chromeVer = chromeVer
        self.__profileName = profileName
        self.__profileLoc = getcwd() + fr"/Profile/{self.__profileName}"


        self.options = ChromeOptions()
        self.options.add_argument(f"user-data-dir={self.__profileLoc}")
        self.options.add_argument("--log-level=3")
        self.options.headless = headless
        self.startBrowser()
        self.login()


    def startBrowser(self):
        self.browser = Chrome(executable_path=self.__chromeDriverPath,options=self.options)
        self.browser.set_window_position(0,0)
        self.browser.set_window_size(1024,768)


    def login(self):
        self.browser.get(self.__whatsappURL)
        wpLoginScreenText = None
        while wpLoginScreenText == None:
            try:
                wpLoginScreenText = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[1]/div').text
            except:
                pass
            try:
                wpLoginScreenText = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[4]/div/div/div[2]/h1').text
            except:
                sleep(0.5)
        if wpLoginScreenText == "WhatsApp'ı bilgisayarınızda kullanmak için":
            self.__isLogin = False
            input("Giriş ekranı var giriş yapın. Ardından enter tuşuna basın")
            try:
                wpLoginScreenText = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[4]/div/div/div[2]/h1').text
                self.__isLogin = True
            except:
                self.__isLogin = False
        else:
            self.__isLogin = True

    def getChromeDriverPath(self):
        return self.__chromeDriverPath
    def setChromeDriverPath(self,newPath):
        self.__chromeDriverPath = newPath

    def getWhatsappURL(self):
        return self.__whatsappURL
    def setWhatsappURL(self,newURL):
        self.__whatsappURL = newURL

    def getCBRememberMe(self) -> bool:
        """Whatsapp giriş sayfasındaki hatırla beni kutucuğunun durumunu döndürür. (True/False -> Bool)"""
        if self.browser.current_url == self.__whatsappURL:
            if self.browser.execute_script("return document.getElementsByName('rememberMe')[0].checked") == True:
                self.__CBRememberMe = True
            else:
                self.__CBRememberMe = False
            return self.__CBRememberMe

    def setCBRememberMe(self,newBool : bool):
        """Whatsapp giriş sayfasındaki hatırla beni kutucuğunun durumunu değiştirir."""
        if self.browser.current_url == self.__whatsappURL:
            activeCBRememberMeStation = self.getCBRememberMe()
            if activeCBRememberMeStation != newBool:
                self.browser.execute_script("document.getElementsByName('rememberMe')[0].click()")
    
    def getLastConversations(self):
        pass


if __name__ == "__main__":
    pass