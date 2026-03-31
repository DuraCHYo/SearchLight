class SecurityService:
    def __init__(self, client):
        self.client = client

    def get_roles(self):
        return self.client.security.get_roles()

    def get_users(self):
        return self.client.security.get_users()

    def get_health(self):
        return self.client.security.health()

    def who_am_i(self):
        return self.client.security.who_am_i()
