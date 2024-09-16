import os
import sys
from pathlib import Path
from utils.extract import extract
from utils.filter import filter_irs_vdc



def process_directory(input_dir: Path, extract_dir: Path, filter_dir: Path):

    extract(input_dir, extract_dir)

    filter_irs_vdc(extract_dir, filter_dir)



def main(input_dir: Path, extract_dir: Path, filter_dir: Path):

    if not os.path.isdir(input_dir):
        print(f"Error: The input directory '{input_dir}' does not exist.")
        sys.exit(1)

    extract_dir.mkdir(parents=True, exist_ok=True)
    filter_dir.mkdir(parents=True, exist_ok=True)

    process_directory(input_dir, extract_dir, filter_dir)



if __name__ == "__main__":

    input_dir = Path('in')
    extract_dir = Path('out/extracted')
    filter_dir = Path('out/filtered')

    main(input_dir, extract_dir, filter_dir)
