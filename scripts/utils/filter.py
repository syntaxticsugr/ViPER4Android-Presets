import os
import shutil
from pathlib import Path



def filter_irs_vdc_xml(input_dir: Path, irs_dir: Path, vdc_dir: Path, xml_dir: Path):

    for root, _, files in os.walk(input_dir):

        for file in files:
            file_path = Path(root)
            full_path = file_path/file

            file_name = full_path.stem
            file_extension = full_path.suffix

            if (file_extension == '.irs'):
                shutil.copy2(full_path, irs_dir)

            elif (file_extension == '.vdc'):
                shutil.copy2(full_path, vdc_dir)

            elif (file_extension == '.xml'):
                if (file_name in ['bt_a2dp', 'headset', 'speaker', 'usb_device']):
                    new_file_name = file_path.stem
                else:
                    new_file_name = file_name

                shutil.copy2(full_path, f'{xml_dir/new_file_name}.xml')
