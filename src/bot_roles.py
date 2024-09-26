class Bot_Role:
    def __init__ (self, name, code):
        self.name = name
        self.code = code

qotdCreator = Bot_Role("Admin", "admin");
qotdCreator = Bot_Role("Moderator", "mod");
qotdCreator = Bot_Role("QOTD Creator", "qotdc");
qotwCreator = Bot_Role("QOTW Creator", "qotwc");