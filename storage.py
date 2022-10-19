communities = {}


def add_community(name, version, port, ip_add):
    communities[name] = [version, port, ip_add]


def delete_community(name):
    del communities[name]


def get_community(name):
    return communities[name]