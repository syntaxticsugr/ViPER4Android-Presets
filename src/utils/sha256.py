import hashlib



def sha256(root):
    hasher = hashlib.sha256()

    with open(root, 'rb') as f:
        for chunk in iter(lambda: f.read(1024), b''):
            hasher.update(chunk)

    return hasher.hexdigest()
