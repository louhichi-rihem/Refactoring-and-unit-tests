import hashlib


def md5(id):
    return hashlib.md5(str(id).encode("utf-8")).hexdigest()


def add_child(etats, orphan):
    for etat in etats:
        if etat["id"] == orphan["id_parent"]:
            orphan["child"] = []
            etat["child"].append(orphan)
            return
        add_child(etat["child"], orphan)
    return
