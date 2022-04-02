import json


class MainSettings:
    with open('modules/token.json', 'r') as file:
        tg_data = json.load(file)

    def tg_token(self):
        return str(self.tg_data['telegram_token'])

    def password_db(self):
        return str(self.tg_data['postgre_password'])

    def user_db(self):
        return str(self.tg_data['postgre_username'])

    def db_host(self):
        return str(self.tg_data['postgre_host'])

    def db_name(self):
        return str(self.tg_data['db_name'])

    def server(self):
        return str(self.tg_data['server_promo_cod'])
