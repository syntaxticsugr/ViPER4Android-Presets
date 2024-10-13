import os
from collections import defaultdict
from pathlib import Path
from utils.create_directories import create_directories
from utils.sha256 import sha256



def check_duplicates(irs_dir: Path, vdc_dir: Path, xml_dir: Path, output_dir: Path):

    output_dir = output_dir/'duplicates'
    create_directories([output_dir])

    irs_hashes = defaultdict(set)
    vdc_hashes = defaultdict(set)
    xml_hashes = defaultdict(set)

    def process_directory(directory: Path, hashes: defaultdict):
        for root, _, files in os.walk(directory):
            root = Path(root)

            for file in files:
                full_path = root/file

                file_name = full_path.stem
                file_name_lower = file_name.lower()

                file_hash = sha256(full_path)

                if file_name_lower not in hashes[file_hash]:
                    hashes[file_hash].add(file_name_lower)

    process_directory(irs_dir, irs_hashes)
    process_directory(vdc_dir, vdc_hashes)
    process_directory(xml_dir, xml_hashes)

    with(
        open(output_dir/'irs_dup.txt', 'w') as irs_dup_txt,
        open(output_dir/'vdc_dup.txt', 'w') as vdc_dup_txt,
        open(output_dir/'xml_dup.txt', 'w') as xml_dup_txt
    ):
        irs_dup = []
        vdc_dup = []
        xml_dup = []

        for key, value in irs_hashes.items():
            irs_dup.append(f'{len(value)} : {key} : {value}\n')

        for key, value in vdc_hashes.items():
            vdc_dup.append(f'{len(value)} : {key} : {value}\n')

        for key, value in xml_hashes.items():
            xml_dup.append(f'{len(value)} : {key} : {value}\n')

        irs_dup = sorted(irs_dup, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)
        vdc_dup = sorted(vdc_dup, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)
        xml_dup = sorted(xml_dup, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)

        irs_dup_txt.writelines(irs_dup)
        vdc_dup_txt.writelines(vdc_dup)
        xml_dup_txt.writelines(xml_dup)
