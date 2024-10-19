from pathlib import Path



def create_directories(directories: list[Path]):

    for dir in directories:
        dir.mkdir(parents=True, exist_ok=True)
