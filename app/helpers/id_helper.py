import secrets


class IdServer:
    # 16位的随机id
    def new(self, prefix):
        random_string = secrets.token_hex(8)
        return prefix + random_string
