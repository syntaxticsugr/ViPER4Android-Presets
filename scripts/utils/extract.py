import os
import shutil
import patoolib
from pathlib import Path
from utils.create_directories import create_directories



def extract(archive_path: Path, extract_to: Path):

    try:
        patoolib.extract_archive(
            str(archive_path),
            outdir = str(extract_to),
            verbosity = -1
        )

    except:
        print(archive_path)



def extract_archives(input_dir: Path, output_dir: Path):

    extract_dir = output_dir/'extracted'
    create_directories([extract_dir])

    for root, _, files in os.walk(input_dir):

        for file in files:
            file_path = Path(root)
            relative_file_path = file_path.relative_to(input_dir)
            full_path = file_path/file

            file_name = full_path.stem
            file_extension = full_path.suffix

            if file_extension in ['.zip', '.rar']:
                save_dir = extract_dir/relative_file_path/file_name
                save_dir.mkdir(parents=True, exist_ok=True)

                extract(full_path, save_dir)
                extract_archives(save_dir, save_dir)

            else:
                try:
                    shutil.copy2(full_path, extract_dir/(full_path.relative_to(input_dir)))
                except:
                    pass

    return extract_dir
