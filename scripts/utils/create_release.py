import os
import shutil
from pathlib import Path



def copy_files(source_dir: Path, destination_dir: Path):
    destination_dir.mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)

        shutil.copy2(source_file, destination_file)



def create_release(ddc_dir: Path, kernel_dir: Path, preset_dir: Path, release_dir: Path, version: str):

    full_ddc = release_dir/'DDC'
    full_kernel = release_dir/'Kernel'
    full_preset = release_dir/'Preset'

    copy_files(ddc_dir, full_ddc)
    copy_files(kernel_dir, full_kernel)
    copy_files(preset_dir, full_preset)
