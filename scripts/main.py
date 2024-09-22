import os
import sys
from pathlib import Path
from utils.convert import convert_presets
from utils.create_release import create_release
from utils.extract import extract_archives
from utils.filter import filter_irs_vdc_xml



def process_directory(input_dir: Path, extract_dir: Path, filter_dir: Path, irs_dir: Path, vdc_dir: Path, xml_dir: Path, preset_converted_dir: Path, release_dir: Path, version: str):

    extract_archives(input_dir, extract_dir)

    filter_irs_vdc_xml(extract_dir, filter_dir, irs_dir, vdc_dir, xml_dir)

    convert_presets(xml_dir, preset_converted_dir)

    create_release(vdc_dir, irs_dir, preset_converted_dir, release_dir, version)



def main(input_dir: Path, output_dir: Path, version: str):

    if not os.path.isdir(input_dir):
        print(f"Error: The input directory '{input_dir}' does not exist.")
        sys.exit(1)

    extract_dir = output_dir/'extracted'
    filter_dir = output_dir/'filtered'
    preset_converted_dir = output_dir/'preset-converted'

    irs_dir = filter_dir/'kernel'
    vdc_dir = filter_dir/'ddc'
    xml_dir = filter_dir/'preset'

    release_dir = output_dir/version

    directories = [
        output_dir,
        extract_dir,
        filter_dir,
        preset_converted_dir,
        irs_dir,
        vdc_dir,
        xml_dir,
        release_dir
    ]

    for dir in directories:
        dir.mkdir(parents=True, exist_ok=True)

    process_directory(input_dir, extract_dir, filter_dir, irs_dir, vdc_dir, xml_dir, preset_converted_dir, release_dir, version)



if __name__ == "__main__":

    version = '2.0.0'

    input_dir = Path('in')
    output_dir = Path('build/output')

    main(input_dir, output_dir, version)
