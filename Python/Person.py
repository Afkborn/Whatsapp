class Person:
    def __init__(self,name,type,findPlace) -> None:
        """Person sınıfından bir obje oluşturur. birinci parametre objenin adını ikinci parametre objenin tipini belirtir. type: 0=>person, 1=>Group    findPlace: 0=>last conversation, 1=>new chat side"""
        self.__name = name
        if type == 0:
            self.__type = "Person"
        else:
            self.__type = "Group"
        if findPlace == 0:
            self.__findPlace = "LastConversation"
        else:
            self.__findPlace = "NewChatSide"
    def getName(self) -> str:
        """return name"""
        return self.__name
    def getType(self) -> str:
        """return type (person,group)"""
        return self.__type
    def getFindPlace(self) -> str:
        """return find place (conversation, new chat side)"""
        return self.__findPlace