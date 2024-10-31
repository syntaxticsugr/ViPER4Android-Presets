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
    full_irs = full_release_dir/'Kernel'
    full_vdc = full_release_dir/'DDC'
    full_xml = full_release_dir/'Preset'
    create_directories([full_release_dir, full_irs, full_vdc, full_xml])

    copy_files(irs_dir, full_irs)
    copy_files(vdc_dir, full_vdc)
    copy_files(xml_dir, full_xml)

    return full_release_dir



def lite_release(irs_dir: Path, vdc_dir: Path, xml_dir: Path, dup_xml_full_txt: Path, release_dir: Path):
    lite_release_dir = release_dir/'Lite'
    lite_irs = lite_release_dir/'Kernel'
    lite_vdc = lite_release_dir/'DDC'
    lite_xml = lite_release_dir/'Preset'
    create_directories([lite_release_dir, lite_irs, lite_vdc, lite_xml])

    with open(dup_xml_full_txt, 'r') as dup_xml:
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



def recommended_release(full_irs_dir: Path, full_vdc_dir: Path, lite_irs_dir: Path, lite_vdc_dir: Path, lite_xml_dir: Path, dup_irs_full_txt: Path, dup_vdc_full_txt: Path, release_dir: Path):
    recommended_release_dir = release_dir/'Recommended'
    recommended_irs = recommended_release_dir/'Kernel'
    recommended_vdc = recommended_release_dir/'DDC'
    recommended_xml = recommended_release_dir/'Preset'
    create_directories([recommended_release_dir, recommended_irs, recommended_vdc, recommended_xml])

    copy_files(lite_irs_dir, recommended_irs)
    copy_files(lite_vdc_dir, recommended_vdc)
    copy_files(lite_xml_dir, recommended_xml)

    present_irss = os.listdir(recommended_irs)
    present_vdcs = os.listdir(recommended_vdc)

    with open(dup_irs_full_txt, 'r') as dup_irs:
        dup_irs_data = dup_irs.readlines()

        for l in dup_irs_data:
            l = l.split(' : ')

            irss = l[-1]
            irss = ast.literal_eval(irss)

            flag = False
            for i in present_irss:
                i = Path(i)
                i = i.stem
                if (i in irss):
                    flag = True
                    break

            if (not flag):
                irs = irss[0]
                irs = full_irs_dir/f'{irs}.irs'
                shutil.copy2(irs, recommended_irs)

    with open(dup_vdc_full_txt, 'r') as dup_vdc:
        dup_vdc_data = dup_vdc.readlines()

        for l in dup_vdc_data:
            l = l.split(' : ')

            vdcs = l[-1]
            vdcs = ast.literal_eval(vdcs)

            flag = False
            for i in present_vdcs:
                i = Path(i)
                i = i.stem
                if (i in vdcs):
                    flag = True
                    break

            if (not flag):
                vdc = vdcs[0]
                vdc = full_vdc_dir/f'{vdc}.vdc'
                shutil.copy2(vdc, recommended_vdc)

    return recommended_release_dir, recommended_irs, recommended_vdc, recommended_xml



def create_release(full_irs_dir: Path, full_vdc_dir: Path, full_xml_dir: Path, output_dir: Path, new_version: str):

    release_dir = output_dir/new_version
    create_directories([release_dir])

    full_release_dir = full_release(full_irs_dir, full_vdc_dir, full_xml_dir, release_dir)
    find_missings(full_irs_dir, full_vdc_dir, full_xml_dir, full_release_dir)
    dup_irs_full_txt, dup_vdc_full_txt, dup_xml_full_txt = check_duplicates(full_irs_dir, full_vdc_dir, full_xml_dir, full_release_dir)

    lite_release_dir, lite_irs_dir, lite_vdc_dir, lite_xml_dir = lite_release(full_irs_dir, full_vdc_dir, full_xml_dir, dup_xml_full_txt, release_dir)
    find_missings(lite_irs_dir, lite_vdc_dir, lite_xml_dir, lite_release_dir)
    _, _, _ = check_duplicates(lite_irs_dir, lite_vdc_dir, lite_xml_dir, lite_release_dir)

    recommended_release_dir, recommended_irs_dir, recommended_vdc_dir, recommended_xml_dir = recommended_release(full_irs_dir, full_vdc_dir, lite_irs_dir, lite_vdc_dir, lite_xml_dir, dup_irs_full_txt, dup_vdc_full_txt, release_dir)
    find_missings(recommended_irs_dir, recommended_vdc_dir, recommended_xml_dir, recommended_release_dir)
    _, _, _ = check_duplicates(recommended_irs_dir, recommended_vdc_dir, recommended_xml_dir, recommended_release_dir)
