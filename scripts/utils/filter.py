import os
import shutil
from pathlib import Path



def filter_irs_vdc(input_dir: Path, output_dir: Path):

    irs_dir = output_dir/'Kernel'
    vdc_dir = output_dir/'DDC'
    xml_dir = output_dir/'Preset'

    irs_dir.mkdir(parents=True, exist_ok=True)
    vdc_dir.mkdir(parents=True, exist_ok=True)
    xml_dir.mkdir(parents=True, exist_ok=True)

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

                shutil.copy2(full_path, f"{str(xml_dir)}/{str(new_file_name)}.xml")
