class User:
    """docstring fos User"""

    def __init__(self, name, email, url, cf_url, cc_url):
        self.name = name
        self.email = email
        self.url = url
        self.cf_url = cf_url
        self.cc_url = cc_url
        self.cf_sol = 0
        self.cc_sol = 0
        self.total_sol = 0

    def get_total_sol(self):
        self.total_sol = self.cf_sol + self.cc_sol
        return (self.total_sol)
