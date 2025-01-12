import ast
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from utils.create_directories import create_directories
from utils.release_utils.check_duplicates import check_duplicates
from utils.release_utils.list_missings import list_missings
from utils.release_utils.search_in_xml import search_in_xml

# Preset (.xml) files whose names contain any of these keywords
# are considered original and selected from duplicates.
whitelist = [
    "Bee", "Devarim", "Deiwid63", "Inner_Fidelity", "J144df",
    "Joe_Meek", "Joemeek", "Percocet", "Roi007leaf", "Stormviper",
    "Smeejaytee", "V4ARISE", "Japanese", "Joe0Bloggs"
]

@dataclass
class ReleaseFiles:
    """Represents the file structure for a release variant"""
    base_dir: Path
    kernel_dir: Path
    ddc_dir: Path
    preset_dir: Path

    @classmethod
    def create(cls, base_path: Path, variant_name: str) -> 'ReleaseFiles':
        base_dir = base_path/variant_name
        kernel_dir = base_dir/'Kernel'
        ddc_dir = base_dir/'DDC'
        preset_dir = base_dir/'Preset'

        create_directories([base_dir, kernel_dir, ddc_dir, preset_dir])
        return cls(base_dir, kernel_dir, ddc_dir, preset_dir)

def copy_directory_contents(source_dir: Path, dest_dir: Path) -> None:
    """Copy all files from source directory to destination directory"""
    for filename in os.listdir(source_dir):
        shutil.copy2(source_dir/filename, dest_dir/filename)

def process_xml_dependencies(xml_path: Path, irs_dir: Path, vdc_dir: Path, target_irs: Path, target_vdc: Path) -> None:
    """Process and copy IRS/VDC files referenced in XML"""
    # Check for IRS dependency
    if irs_path := search_in_xml(xml_path, "65540;65541;65542"):
        try:
            shutil.copy2(irs_dir/irs_path, target_irs)
        except (FileNotFoundError, shutil.Error):
            pass

    # Check for VDC dependency
    if vdc_path := search_in_xml(xml_path, "65547"):
        try:
            shutil.copy2(vdc_dir/vdc_path, target_vdc)
        except (FileNotFoundError, shutil.Error):
            pass

def select_whitelist_xml(xml_list: list[str], whitelist: list[str]) -> str:
    """
    Select XML name from the list based on whitelist criteria.
    Returns the first matching name after sorting, or the first name in original list if no matches.
    """
    # Find all names containing whitelist words
    matching_names = [
        name for name in xml_list
        if any(word.lower() in name.lower() for word in whitelist)
    ]

    # If we found matches, sort them and return the first one
    if matching_names:
        return sorted(matching_names)[0]

    # If no matches, return the first name from original list
    return xml_list[0]

def create_full_release(source: ReleaseFiles, release_dir: Path) -> ReleaseFiles:
    """Create full release"""
    full = ReleaseFiles.create(release_dir, 'Full')

    copy_directory_contents(source.kernel_dir, full.kernel_dir)
    copy_directory_contents(source.ddc_dir, full.ddc_dir)
    copy_directory_contents(source.preset_dir, full.preset_dir)

    return full

def create_lite_release(source: ReleaseFiles, release_dir: Path, dup_files: tuple[Path, Path, Path]) -> ReleaseFiles:
    """Create lite release"""
    lite = ReleaseFiles.create(release_dir, 'Lite')
    _, _, dup_xml_path = dup_files

    with open(dup_xml_path, 'r') as f:
        for line in f:
            parts = line.split(' : ')
            count = int(parts[0])  # Number of duplicates
            xml_list = ast.literal_eval(parts[-1])

            # Only apply whitelist selection for groups with duplicates
            if count > 1:
                xml_name = select_whitelist_xml(xml_list, whitelist)
            else:
                xml_name = xml_list[0]

            xml_path = source.preset_dir/f'{xml_name}.xml'

            # Copy XML and its dependencies
            shutil.copy2(xml_path, lite.preset_dir)
            process_xml_dependencies(xml_path, source.kernel_dir, source.ddc_dir, lite.kernel_dir, lite.ddc_dir)

    return lite

def create_recommended_release(full: ReleaseFiles, lite: ReleaseFiles, release_dir: Path, dup_files: tuple[Path, Path, Path]) -> ReleaseFiles:
    """Create recommended release"""
    recommended = ReleaseFiles.create(release_dir, 'Recommended')
    dup_irs_path, dup_vdc_path, _ = dup_files

    # Start with lite contents
    copy_directory_contents(lite.kernel_dir, recommended.kernel_dir)
    copy_directory_contents(lite.ddc_dir, recommended.ddc_dir)
    copy_directory_contents(lite.preset_dir, recommended.preset_dir)

    # Process IRS duplicates
    present_irs = {Path(f).stem for f in os.listdir(recommended.kernel_dir)}
    with open(dup_irs_path, 'r') as f:
        for line in f:
            irs_list = ast.literal_eval(line.split(' : ')[-1])
            if not any(irs in present_irs for irs in irs_list):
                shutil.copy2(full.kernel_dir/f'{irs_list[0]}.irs', recommended.kernel_dir)

    # Process VDC duplicates
    present_vdc = {Path(f).stem for f in os.listdir(recommended.ddc_dir)}
    with open(dup_vdc_path, 'r') as f:
        for line in f:
            vdc_list = ast.literal_eval(line.split(' : ')[-1])
            if not any(vdc in present_vdc for vdc in vdc_list):
                shutil.copy2(full.ddc_dir/f'{vdc_list[0]}.vdc', recommended.ddc_dir)

    return recommended

def create_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, output_dir: Path, version: str) -> Path:
    """Create new release with 3 variants - Full, Lite & Recommended"""
    print(f"Creating Release {version} ...")

    release_dir = output_dir/version
    create_directories([release_dir])

    # Create source structure
    source = ReleaseFiles(release_dir, irs_dir, vdc_dir, xml_dir)

    # Create full release
    full = create_full_release(source, release_dir)
    list_missings(full.kernel_dir, full.ddc_dir, full.preset_dir, full.base_dir)
    dup_files = check_duplicates(full.kernel_dir, full.ddc_dir, full.preset_dir, full.base_dir)

    # Create lite release
    lite = create_lite_release(source, release_dir, dup_files)
    list_missings(lite.kernel_dir, lite.ddc_dir, lite.preset_dir, lite.base_dir)
    check_duplicates(lite.kernel_dir, lite.ddc_dir, lite.preset_dir, lite.base_dir)

    # Create recommended release
    recommended = create_recommended_release(full, lite, release_dir, dup_files)
    list_missings(recommended.kernel_dir, recommended.ddc_dir, recommended.preset_dir, recommended.base_dir)
    check_duplicates(recommended.kernel_dir, recommended.ddc_dir, recommended.preset_dir, recommended.base_dir)

    return release_dir
