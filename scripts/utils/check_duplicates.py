import os
from collections import defaultdict
from pathlib import Path
from utils.create_directories import create_directories
from utils.sha256 import sha256



def write_duplicates_to_file(hashes: defaultdict, filename: Path):
    with open(filename, 'w') as dup_txt:
        duplicates = []

        for key, value in hashes.items():
            value = sorted(value)
            duplicates.append(f'{len(value)} : {key} : {value}\n')

        duplicates = sorted(duplicates, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)

        dup_txt.writelines(duplicates)



def process_directory(directory: Path, hashes: defaultdict):
    for root, _, files in os.walk(directory):
        root = Path(root)

        for file in files:
            full_path = root/file

            file_name = full_path.stem

            file_hash = sha256(full_path)

            if file_name not in hashes[file_hash]:
                hashes[file_hash].add(file_name)



def check_duplicates(irs_dir: Path, vdc_dir: Path, xml_dir: Path, output_dir: Path):

    output_dir = output_dir/'duplicates'
    create_directories([output_dir])

    irs_hashes = defaultdict(set)
    vdc_hashes = defaultdict(set)
    xml_hashes = defaultdict(set)

    process_directory(irs_dir, irs_hashes)
    process_directory(vdc_dir, vdc_hashes)
    process_directory(xml_dir, xml_hashes)

    dup_irs_txt = output_dir/'dup_irs.txt'
    dup_vdc_txt = output_dir/'dup_vdc.txt'
    dup_xml_txt = output_dir/'dup_xml.txt'

    write_duplicates_to_file(irs_hashes, dup_irs_txt)
    write_duplicates_to_file(vdc_hashes, dup_vdc_txt)
    write_duplicates_to_file(xml_hashes, dup_xml_txt)

    return(dup_irs_txt, dup_vdc_txt, dup_xml_txt)
