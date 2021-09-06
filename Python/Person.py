class Person:
    def __init__(self,name,type) -> None:
        """Person sınıfından bir obje oluşturur. birinci parametre objenin adını ikinci parametre objenin tipini belirtir. 0=>person, 1=>Group"""
        self.__name = name
        if type == 0:
            self.__type = "Person"
        else:
            self.__type = "Group"
    def getName(self):
        """return name"""
        return self.__name
    def getType(self):
        """return type (person,group)"""
        return self.__type