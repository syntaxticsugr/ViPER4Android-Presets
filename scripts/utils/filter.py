import os
import hashlib
import shutil
from collections import defaultdict
from pathlib import Path



def get_new_suffix(path: Path, suffix=2):
    if (Path(f'{path}_{suffix}').is_file()):
        get_new_suffix(path, suffix=(suffix+1))
    else:
        return suffix



def sha256(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()



def filter_irs_vdc_xml(input_dir: Path, filter_dir: Path, irs_dir: Path, vdc_dir: Path, xml_dir: Path):

    irs_hashes = defaultdict(set)
    vdc_hashes = defaultdict(set)
    xml_hashes = defaultdict(set)

    for root, _, files in os.walk(input_dir):

        for file in files:
            file_path = Path(root)
            full_path = file_path/file

            file_name = full_path.stem.lower()
            file_extension = full_path.suffix

            file_hash = sha256(full_path)

            if (file_extension == '.irs'):
                if (file_name not in irs_hashes[file_hash]):
                    irs_hashes[file_hash].add(file_name)

                    filtered_irs = Path(f'{irs_dir/file_name}.irs')
                    if (filtered_irs.is_file()):
                        file_name = f'{file_name}_{get_new_suffix(filtered_irs)}'

                    shutil.copy2(full_path, f'{irs_dir/file_name}.irs')

            elif (file_extension == '.vdc'):
                if (file_name not in vdc_hashes[file_hash]):
                    vdc_hashes[file_hash].add(file_name)

                    filtered_vdc = Path(f'{vdc_dir/file_name}.vdc')
                    if (filtered_vdc.is_file()):
                        file_name = f'{file_name}_{get_new_suffix(filtered_vdc)}'

                    shutil.copy2(full_path, f'{vdc_dir/file_name}.vdc')

            elif (file_extension == '.xml'):
                if (file_name in ['bt_a2dp', 'headset', 'speaker', 'usb_device']):
                    file_name = f'{file_path.stem}{file_path.suffix}-{file_name}'.lower()

                if (file_name not in xml_hashes[file_hash]):
                    xml_hashes[file_hash].add(file_name)

                    filtered_xml = Path(f'{xml_dir/file_name}.xml')
                    if (filtered_xml.is_file()):
                        file_name = f'{file_name}_{get_new_suffix(filtered_xml)}'

                    shutil.copy2(full_path, f'{xml_dir/file_name}.xml')

    with(
        open(filter_dir/'irs_dup.txt', 'w') as irs_dup_txt,
        open(filter_dir/'vdc_dup.txt', 'w') as vdc_dup_txt,
        open(filter_dir/'xml_dup.txt', 'w') as xml_dup_txt
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

        irs_dup.sort()
        vdc_dup.sort()
        xml_dup.sort()

        irs_dup_txt.writelines(irs_dup)
        vdc_dup_txt.writelines(vdc_dup)
        xml_dup_txt.writelines(xml_dup)
