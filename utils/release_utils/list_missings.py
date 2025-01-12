import os
from collections import defaultdict
from pathlib import Path
from utils.release_utils.search_in_xml import search_in_xml

def list_missings(irs_dir: Path, vdc_dir: Path, xml_dir: Path, output_dir: Path) -> None:
    """List missing IRSs & VDCs in missing.txt"""

    missing_irs = defaultdict(set)
    missing_vdc = defaultdict(set)

    for root, _, files in os.walk(xml_dir):
        root = Path(root)

        for file in files:
            xml = root/file

            irs = search_in_xml(xml, "65540;65541;65542")
            if ((irs != None) and not (os.path.isfile(irs_dir/irs))):
                missing_irs[irs].add(file)

            vdc = search_in_xml(xml, "65547")
            if ((vdc != None) and not (os.path.isfile(vdc_dir/vdc))):
                missing_vdc[vdc].add(file)

    with open(output_dir/'missing.txt', 'w') as file:
        missing = ["[IRS]\n"]

        temp_missing = []
        for key, value in missing_irs.items():
            value = sorted(value)
            temp_missing.append(f'{len(value)} : {key} : {value}\n')

        temp_missing = sorted(temp_missing, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)
        missing.extend(temp_missing)

        missing.append("\n[VDC]\n")

        temp_missing = []
        for key, value in missing_vdc.items():
            value = sorted(value)
            temp_missing.append(f'{len(value)} : {key} : {value}\n')

        temp_missing = sorted(temp_missing, key=lambda x: (int(x.split(' : ')[0]), x.split(' : ')[1]), reverse=True)
        missing.extend(temp_missing)

        file.writelines(missing)
