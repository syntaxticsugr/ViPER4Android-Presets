import ast
import os
import shutil
from pathlib import Path
from utils.check_duplicates import check_duplicates
from utils.create_directories import create_directories
from utils.find_missings import find_missings
from utils.search_in_xml import search_in_xml



def copy_files(source_dir: Path, destination_dir: Path):

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)

        shutil.copy2(source_file, destination_file)



def full_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, release_dir: Path):
    full_release_dir = release_dir/'Full'
    full_vdc = full_release_dir/'DDC'
    full_irs = full_release_dir/'Kernel'
    full_xml = full_release_dir/'Preset'
    create_directories([full_release_dir, full_vdc, full_irs, full_xml])

    copy_files(irs_dir, full_irs)
    copy_files(vdc_dir, full_vdc)
    copy_files(xml_dir, full_xml)

    return full_release_dir



def lite_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, dup_xml_txt: Path, release_dir: Path):
    lite_release_dir = release_dir/'Lite'
    lite_vdc = lite_release_dir/'DDC'
    lite_irs = lite_release_dir/'Kernel'
    lite_xml = lite_release_dir/'Preset'
    create_directories([lite_release_dir, lite_vdc, lite_irs, lite_xml])

    with open(dup_xml_txt, 'r') as dup_xml:
        dup_xml_data = dup_xml.readlines()

        for l in dup_xml_data:
            l = l.split(' : ')

            xmls = l[-1]
            xmls = ast.literal_eval(xmls)

            xml = xmls[0]
            xml = xml_dir/f'{xml}.xml'
            shutil.copy2(xml, lite_xml)

            irs = search_in_xml(xml, "65540;65541;65542")
            if (irs != None):
                irs = irs_dir/irs
                try:
                    shutil.copy2(irs, lite_irs)
                except:
                    pass

            vdc = search_in_xml(xml, "65547")
            if (vdc != None):
                vdc = vdc_dir/vdc
                try:
                    shutil.copy2(vdc, lite_vdc)
                except:
                    pass

    return(lite_release_dir, lite_irs, lite_vdc, lite_xml)



def create_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, output_dir: Path, new_version: str):

    release_dir = output_dir/new_version
    create_directories([release_dir])

    full_release_dir = full_release(irs_dir, vdc_dir, xml_dir, release_dir)

    find_missings(irs_dir, vdc_dir, xml_dir, full_release_dir)

    dup_irs_txt, dup_vdc_txt, dup_xml_txt = check_duplicates(irs_dir, vdc_dir, xml_dir, full_release_dir)

    lite_release_dir, lite_irs_dir, lite_vdc_dir, lite_xml_dir = lite_release(irs_dir, vdc_dir, xml_dir, dup_xml_txt, release_dir)

    find_missings(irs_dir, vdc_dir, lite_xml_dir, lite_release_dir)

    dup_irs_lite_txt, dup_vdc_lite_txt, dup_xml_lite_txt = check_duplicates(lite_irs_dir, lite_vdc_dir, lite_xml_dir, lite_release_dir)
