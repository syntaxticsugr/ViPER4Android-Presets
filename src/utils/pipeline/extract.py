import os
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

    except Exception as e:
        print(f'Failed to extract "{archive_path}" - {e}')



def extract_archives(input_dir: Path, output_dir: Path):

    extract_dir = output_dir/'extracted'
    create_directories([extract_dir])

    directories_to_process = [input_dir]

    while directories_to_process:
        current_dir = directories_to_process.pop()

        for root, _, files in os.walk(current_dir):
            root = Path(root)

            for file in files:
                full_path = root/file

                try:
                    relative_file_path = root.relative_to(input_dir)
                except:
                    relative_file_path = root.relative_to(extract_dir)

                file_name = full_path.stem
                file_extension = full_path.suffix

                if file_extension in ['.zip', '.rar', '.tar']:

                    save_dir = extract_dir/relative_file_path/file_name

                    count = 1
                    while (save_dir.exists()):
                        count += 1
                        save_dir = Path(f'{save_dir}_{count}')

                    save_dir.mkdir(parents=True, exist_ok=True)

                    extract(full_path, save_dir)

                    directories_to_process.append(save_dir)

    return extract_dir
