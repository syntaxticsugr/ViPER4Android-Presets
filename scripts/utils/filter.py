import os
import shutil
from collections import defaultdict
from pathlib import Path
from utils.create_directories import create_directories
from utils.sha256 import sha256



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
            file_extension = full_path.suffix

            file_hash = sha256(full_path)

            if (file_extension == '.irs'):
                if (file_name not in irs_hashes[file_hash]):
                    irs_hashes[file_hash].add(file_name)

                    name_repeat_count = IRSs[file_name]
                    name_repeat_count += 1
                    IRSs[file_name] = name_repeat_count

                    if (1 < name_repeat_count):
                        new_file_name = f'{file_name}_{name_repeat_count}'

                    shutil.copy2(full_path, f'{irs_dir/new_file_name}.irs')

            elif (file_extension == '.vdc'):
                if (file_name not in vdc_hashes[file_hash]):
                    vdc_hashes[file_hash].add(file_name)

                    name_repeat_count = VDCs[file_name]
                    name_repeat_count += 1
                    VDCs[file_name] = name_repeat_count

                    if (1 < name_repeat_count):
                        new_file_name = f'{file_name}_{name_repeat_count}'

                    shutil.copy2(full_path, f'{vdc_dir/new_file_name}.vdc')

            elif (file_extension == '.xml'):
                if (file_name in ['bt_a2dp', 'headset', 'speaker', 'usb_device']):
                    new_file_name = f'{root.stem}{root.suffix}'

                if (new_file_name not in xml_hashes[file_hash]):
                    xml_hashes[file_hash].add(new_file_name)

                    name_repeat_count = XMLs[new_file_name]
                    name_repeat_count += 1
                    XMLs[new_file_name] = name_repeat_count

                    if (1 < name_repeat_count):
                        new_file_name = f'{new_file_name}_{name_repeat_count}'

                    shutil.copy2(full_path, f'{xml_dir/new_file_name}.xml')

    return(irs_dir, vdc_dir, xml_dir)
