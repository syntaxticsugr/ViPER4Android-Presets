import os
import sys
from pathlib import Path
from pipe.convert import convert_presets
from pipe.extract import extract_archives
from pipe.filter import filter_irs_vdc_xml
from pipe.release import create_release
from utils.create_directories import create_directories

def process(input_dir: Path, output_dir: Path, version: str):
    extract_dir = extract_archives(input_dir, output_dir)
    irs_dir, vdc_dir, xml_dir = filter_irs_vdc_xml(extract_dir, output_dir)
    preset_converted_dir = convert_presets(xml_dir, output_dir)
    release_dir = create_release(irs_dir, vdc_dir, preset_converted_dir, output_dir, version)
    print(f"Files Saved In: {release_dir}")

def main(input_dir: Path, output_dir: Path, version: str):
    if not os.path.isdir(input_dir):
        print(f"Error: The input directory '{input_dir}' does not exist.")
        sys.exit(1)

    create_directories([output_dir])
    process(input_dir, output_dir, version)

if __name__ == "__main__":

    version = '2.2.0'

    input_dir = Path('in')
    output_dir = Path('build/output')

    main(input_dir, output_dir, version)
