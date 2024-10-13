def create_directories(directories: list):

    for dir in directories:
        dir.mkdir(parents=True, exist_ok=True)
