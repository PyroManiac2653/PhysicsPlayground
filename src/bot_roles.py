class Bot_Role:
    def __init__ (self, name, code):
        self.name = name
        self.code = code
        
role_admin = Bot_Role("Admin", "admin");
role_mod = Bot_Role("Moderator", "mod");
role_qotdCreator = Bot_Role("QOTD Creator", "qotdc");
role_qotwCreator = Bot_Role("QOTW Creator", "qotwc");

all_bot_roles = [role_admin. role_mod, role_qotdCreator, role_qotwCreator]

class Guild_Role_Map:
    def __init__ (self, guild_id, guild_role, bot_role):
        self.guild_id = guild_id
        self.guild_role = guild_role
        if bot_role in all_bot_roles:
            self.bot_rule = bot_role
        else:
            raise ValueError("Invalid bot role")