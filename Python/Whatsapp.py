from os import getcwd, stat
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import get_clock_info, sleep 
from Python.Person import Person
class Whatsapp: 
    __chromeDriverPath = getcwd() +  fr"/Driver/chromedriver.exe"
    __whatsappURL = "https://web.whatsapp.com/"
    def __init__(self,chromeVer,profileName,headless = False) -> None:
        self.__chromeVer = chromeVer
        self.__profileName = profileName
        self.__profileLoc = getcwd() + fr"/Profile/{self.__profileName}"


        self.options = ChromeOptions()
        self.options.add_argument(f"user-data-dir={self.__profileLoc}")
        self.options.add_argument("--lang=tr")
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
        sleep(1)

    def getChromeDriverPath(self):
        """return active chrome driver path"""
        return self.__chromeDriverPath
    def setChromeDriverPath(self,newPath):
        """set new chrome driver path"""
        self.__chromeDriverPath = newPath

    def getWhatsappURL(self):
        """return whatsapp url. default url: 'https://web.whatsapp.com/'"""
        return self.__whatsappURL
    def setWhatsappURL(self,newURL):
        """set new whatsapp url. format: htpps://URL.COM"""
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
    
    def getPersonFromLastConversations(self):
        """Son konuşmalardan kişi isim bilgilerini çeker."""
        nameSet = set()
        for _ in range(30):
            for i in range(1,17):
                try:
                    try:
                        # for person
                        name = self.browser.find_element_by_xpath(f'//*[@id="pane-side"]/div[2]/div/div/div[{i}]/div/div/div[2]/div[1]/div[1]/span/span').text
                        gp = self.browser.find_element_by_xpath(f'//*[@id="pane-side"]/div[2]/div/div/div[{i}]/div/div/div[1]/div/div/div/span').get_attribute('data-testid')
                    except:
                        pass
                    try:

                        # for group 
                        name = self.browser.find_element_by_xpath(f'//*[@id="pane-side"]/div[2]/div/div/div[{i}]/div/div/div[2]/div[1]/div[1]/span').text
                        gp = self.browser.find_element_by_xpath(f'//*[@id="pane-side"]/div[2]/div/div/div[{i}]/div/div/div[1]/div/div/div/span').get_attribute('data-testid')
                    except:
                        pass
                    if gp == "default-group":
                        name = f"{name},GROUP"
                    elif gp == "default-user":
                        name = f"{name},PERSON"
                    if not ",PERSON,PERSON" in name:
                        nameSet.add(name)
                except:
                    pass
            self.__scroolPaneSide(100)
        self.personObj = []
        for i in nameSet:
            if ",PERSON" in i:
                name = i.replace(',PERSON',"")
                myPerson = Person(name,0,0)
            else:
                name = i.replace(",GROUP","")
                myPerson = Person(name,1,0)
            
            self.personObj.append(myPerson)
        
    def __checkName(self,name):
        """name değişkenin self.personObj içinde olup olmadığını kontrol eder eğer var ise True, yok ise False döner."""
        for i in self.personObj:
            iName = i.getName()
            if iName == name:
                return True
        return False

    def getPersonFromNewChatPart(self):
        """Yeni sohbet ekranından kişileri çekmeye yarayan fonksiyon. """
        self.__clickNewChatButton()
        sleep(0.5)
        nameSet = set()
        for _ in range(150):
            for i in range(17):
                try:
                    name = self.browser.find_element_by_xpath(f'//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div/div[{i}]/div/div/div[2]/div[1]/div/span/span').text
                    nameSet.add(name)
                except:
                    pass
            self.__scroolNewChatPartPaneSide(200)
        nameList = list(nameSet)
        for i in nameList:
            if not self.__checkName(i):
                myPerson = Person(i,0,1)
                self.personObj.append(myPerson)

    def __getPersonOBJ(self,name) -> Person:
        """Adı verilen kullanıcının person objesini döner"""
        for i in self.personObj:
            iName = i.getName()
            if iName == name:
                return i
  

            
    def __scroolPaneSide(self,y):
        script = f"""myElement = document.getElementById('pane-side')
        myElement.scrollBy(0,{y})"""
        if self.__isLogin and self.browser.current_url == self.__whatsappURL:
            self.browser.execute_script(script)
        
    def __scroolNewChatPartPaneSide(self,y):
        """Yeni sohbet oluştur panelinde scrool yapmaya yarayan fonksiyon. Y ne kadar scrool yapılacağını belirtir."""
        script = f"""
        function getElementByXpath(path){{
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }}
        myObj1 = getElementByXpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]')
        myObj1.scrollBy(0,{y})
        """
        if self.__isLogin and self.browser.current_url == self.__whatsappURL:
            self.browser.execute_script(script)

    def __clickNewChatButton(self):
        """Yeni sohbet oluştur butonuna tıklar"""
        script = f"""var myObj = document.querySelector('[title="Yeni sohbet"]');
        myObj.click()"""
        if self.__isLogin and self.browser.current_url == self.__whatsappURL:
            self.browser.execute_script(script)
            sleep(0.1)
    
    def printPerson(self):
        """objeye kayıt edilen kişileri yazdırır."""
        for person in self.personObj:
            print(f"Name: {person.getName()} Type: {person.getType()}")

    def searchPeopleInNewChatSide(self,name):
        """Yeni sohbet ekranındaki arama kısmına verilen ismi yazar ve verilen isimle eşleşen bir kişi varsa tıklar ardından True döner."""
        xpath = '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[1]/div/label/div/div[2]'
        searchBox = self.browser.find_element_by_xpath(xpath)
        searchBox.send_keys(name)
        sleep(0.1)
        for i in range(1,6):
            xpath = f'//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[1]/div/div/div[{i}]/div/div/div[2]/div[1]/div/span/span'
            try:
                findObj = self.browser.find_element_by_xpath(xpath)
                if findObj.text == name:
                    findObj.click()
                    return True
            except:
                pass
    def __pressSend(self):
        script = f"""
        function getElementByXpath(path){{
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }}
        myButton = getElementByXpath("//*[@id='main']/footer/div[1]/div/div/div[2]/div[2]/button")
        myButton.click()
        """
        if self.__isLogin and self.browser.current_url == self.__whatsappURL:
            self.browser.execute_script(script)

    def getPersonDetail(self,name):
        if self.__isLogin and self.browser.current_url == self.__whatsappURL and self.__checkName(name): # giriş yapılıp yapılmadığını kontrol et
            myPerson = self.__getPersonOBJ(name) #fonksiyona verilen name adındaki objeyi al
            self.__clickNewChatButton() 
            if self.searchPeopleInNewChatSide(myPerson.getName()):
                #get detail
                pass

    def writeText(self,personName,message):
        if self.__isLogin and self.__checkName(personName) and self.browser.current_url == self.__whatsappURL:
            self.__clickNewChatButton() 
            if self.searchPeopleInNewChatSide(personName):
                myTextBox = self.browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')
                myTextBox.send_keys(message)
                self.__pressSend()

            else:
                print("sex")



if __name__ == "__main__":
    pass