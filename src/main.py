import os
import sys
from pathlib import Path
from utils.create_directories import create_directories
from utils.pipeline.convert import convert_presets
from utils.pipeline.create_release import create_release
from utils.pipeline.extract import extract_archives
from utils.pipeline.filter import filter_irs_vdc_xml



def process_directory(input_dir: Path, output_dir: Path, new_version: str):

    extract_dir = extract_archives(input_dir, output_dir)

    irs_dir, vdc_dir, xml_dir = filter_irs_vdc_xml(extract_dir, output_dir)

    preset_converted_dir = convert_presets(xml_dir, output_dir)

    create_release(irs_dir, vdc_dir, preset_converted_dir, output_dir, new_version)



def main(input_dir: Path, output_dir: Path, new_version: str):

    if not os.path.isdir(input_dir):
        print(f"Error: The input directory '{input_dir}' does not exist.")
        sys.exit(1)

    create_directories([output_dir])

    process_directory(input_dir, output_dir, new_version)



if __name__ == "__main__":

    new_version = '2.1.0'

    input_dir = Path('in')
    output_dir = Path('build/output')

    main(input_dir, output_dir, new_version)
