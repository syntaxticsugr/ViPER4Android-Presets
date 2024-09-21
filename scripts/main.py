import os
import sys
from pathlib import Path
from utils.extract import extract_archives
from utils.filter import filter_irs_vdc_xml
from utils.convert import convert_presets



def process_directory(input_dir: Path, extract_dir: Path, filter_dir: Path, irs_dir: Path, vdc_dir: Path, xml_dir: Path, preset_converted_dir: Path):

    extract_archives(input_dir, extract_dir)

    filter_irs_vdc_xml(extract_dir, filter_dir, irs_dir, vdc_dir, xml_dir)

    convert_presets(xml_dir, preset_converted_dir)



def main(input_dir: Path, extract_dir: Path, filter_dir: Path, preset_converted_dir: Path):

    if not os.path.isdir(input_dir):
        print(f"Error: The input directory '{input_dir}' does not exist.")
        sys.exit(1)


    irs_dir = filter_dir/'kernel'
    vdc_dir = filter_dir/'ddc'
    xml_dir = filter_dir/'preset'

    directories = [
        extract_dir,
        filter_dir,
        irs_dir,
        vdc_dir,
        xml_dir,
        preset_converted_dir
    ]

    for dir in directories:
        dir.mkdir(parents=True, exist_ok=True)

    process_directory(input_dir, extract_dir, filter_dir, irs_dir, vdc_dir, xml_dir, preset_converted_dir)



if __name__ == "__main__":

    input_dir = Path('in')
    extract_dir = Path('out/extracted')
    filter_dir = Path('out/filtered')
    preset_converted_dir = Path('out/preset-converted')

    main(input_dir, extract_dir, filter_dir, preset_converted_dir)
