import os
import hashlib
import shutil
from collections import defaultdict
from pathlib import Path
from utils.create_directories import create_directories



def sha256(root):
    hasher = hashlib.sha256()
    with open(root, 'rb') as f:
        for chunk in iter(lambda: f.read(1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()



def filter_irs_vdc_xml(input_dir: Path, output_dir: Path):

    filter_dir = output_dir/'filtered'
    irs_dir = filter_dir/'kernel'
    vdc_dir = filter_dir/'ddc'
    xml_dir = filter_dir/'preset'

    create_directories([filter_dir, irs_dir, vdc_dir, xml_dir])

    IRSs = defaultdict(int)
    VDCs = defaultdict(int)
    XMLs = defaultdict(int)

    irs_hashes = defaultdict(set)
    vdc_hashes = defaultdict(set)
    xml_hashes = defaultdict(set)

    for root, _, files in os.walk(input_dir):
        root = Path(root)

        for file in files:
            full_path = root/file

            file_name = new_file_name = full_path.stem
            file_name_lower = file_name.lower()
            file_extension = full_path.suffix

            file_hash = sha256(full_path)

            if (file_extension == '.irs'):
                if (file_name_lower not in irs_hashes[file_hash]):
                    irs_hashes[file_hash].add(file_name_lower)

                    name_repeat_count = IRSs[file_name_lower]
                    name_repeat_count += 1
                    IRSs[file_name_lower] = name_repeat_count

                    if (1 < name_repeat_count):
                        new_file_name = f'{file_name}_{name_repeat_count}'

                    shutil.copy2(full_path, f'{irs_dir/new_file_name}.irs')

            elif (file_extension == '.vdc'):
                if (file_name_lower not in vdc_hashes[file_hash]):
                    vdc_hashes[file_hash].add(file_name_lower)

                    name_repeat_count = VDCs[file_name_lower]
                    name_repeat_count += 1
                    VDCs[file_name_lower] = name_repeat_count

                    if (1 < name_repeat_count):
                        new_file_name = f'{file_name}_{name_repeat_count}'

                    shutil.copy2(full_path, f'{vdc_dir/new_file_name}.vdc')

            elif (file_extension == '.xml'):
                if (file_name_lower in ['bt_a2dp', 'headset', 'speaker', 'usb_device']):
                    new_file_name = f'{root.stem}{root.suffix}-{file_name_lower}'

                new_file_name_lower = new_file_name.lower()

                if (new_file_name_lower not in xml_hashes[file_hash]):
                    xml_hashes[file_hash].add(new_file_name_lower)

                    name_repeat_count = XMLs[new_file_name_lower]
                    name_repeat_count += 1
                    XMLs[new_file_name_lower] = name_repeat_count

                    if (1 < name_repeat_count):
                        new_file_name = f'{new_file_name}_{name_repeat_count}'

                    shutil.copy2(full_path, f'{xml_dir/new_file_name}.xml')

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

        irs_dup = sorted(irs_dup, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)
        vdc_dup = sorted(vdc_dup, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)
        xml_dup = sorted(xml_dup, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)

        irs_dup_txt.writelines(irs_dup)
        vdc_dup_txt.writelines(vdc_dup)
        xml_dup_txt.writelines(xml_dup)

    return(irs_dir, vdc_dir, xml_dir)
