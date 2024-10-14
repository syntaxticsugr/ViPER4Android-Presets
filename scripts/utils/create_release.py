import ast
import os
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from utils.create_directories import create_directories



def copy_files(source_dir: Path, destination_dir: Path):

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)

        shutil.copy2(source_file, destination_file)



def full_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, release_dir: Path):
    full_release_dir = release_dir/'Full'
    full_ddc = full_release_dir/'DDC'
    full_kernel = full_release_dir/'Kernel'
    full_preset = full_release_dir/'Preset'
    create_directories([full_release_dir, full_ddc, full_kernel, full_preset])

    copy_files(irs_dir, full_kernel)
    copy_files(vdc_dir, full_ddc)
    copy_files(xml_dir, full_preset)



def search_value_in_xml(xml: Path, key: str):
    tree = ET.parse(xml)
    root = tree.getroot()

    for elem in root.findall('.//'):
        if elem.get('name') == key:
            return elem.text or elem.get('value')

    return None



def lite_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, dup_xml_txt: Path, release_dir: Path):
    lite_release_dir = release_dir/'Lite'
    lite_ddc = lite_release_dir/'DDC'
    lite_kernel = lite_release_dir/'Kernel'
    lite_preset = lite_release_dir/'Preset'
    create_directories([lite_release_dir, lite_ddc, lite_kernel, lite_preset])

    missing_irs = defaultdict(set)
    missing_vdc = defaultdict(set)

    with open(dup_xml_txt, 'r') as dup_xml:
        dup_xml_data = dup_xml.readlines()

        for l in dup_xml_data:
            l = l.split(' : ')

            xmls = l[-1]
            xmls = ast.literal_eval(xmls)

            xml = xmls[0]
            xml = xml_dir/f'{xml}.xml'
            shutil.copy2(xml, lite_preset)

            vdc = search_value_in_xml(xml, "65547")
            if vdc != None:
                vdc = vdc_dir/vdc
                try:
                    shutil.copy2(vdc, lite_ddc)
                except:
                    vdc = os.path.basename(vdc)
                    missing_vdc[vdc].add(xmls[0])

            irs = search_value_in_xml(xml, "65540;65541;65542")
            if irs != None:
                irs = irs_dir/irs
                try:
                    shutil.copy2(irs, lite_kernel)
                except:
                    irs = os.path.basename(irs)
                    missing_irs[irs].add(xmls[0])

    with open(lite_release_dir/'missing.txt', 'w') as file:
        missing = []

        for key, value in missing_irs.items():
            value = sorted(value)
            missing.append(f'{key} : {value}\n')

        missing.append("\n\n\n")

        for key, value in missing_vdc.items():
            value = sorted(value)
            missing.append(f'{key} : {value}\n')

        file.writelines(missing)



def create_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, dup_irs_txt: Path, dup_vdc_txt: Path, dup_xml_txt: Path, output_dir: Path, new_version: str):

    release_dir = output_dir/new_version
    create_directories([release_dir])

    full_release(irs_dir, vdc_dir, xml_dir, release_dir)

    lite_release(irs_dir, vdc_dir, xml_dir, dup_xml_txt, release_dir)
