from pathlib import Path



def check_viper_xml(xml_path: Path):

    with open(xml_path, 'r') as xml_file:
        xml_data = [line.strip() for line in xml_file.readlines()]

        # Master Switch
        check_features = ['<boolean name="36868"']

        check_result = all(any(feature in xml_line for xml_line in xml_data) for feature in check_features)

    return check_result
