import os
from pathlib import Path
from utils.create_directories import create_directories



def convert_presets(input_dir: Path, output_dir: Path):

    preset_converted_dir = output_dir/'preset-converted'
    create_directories([preset_converted_dir])

    default_m1_preset_file = Path('scripts/utils/default_presets/default_m1.xml')
    default_m2_preset_file = Path('scripts/utils/default_presets/default_m2.xml')

    # List of input Presets
    presets = os.listdir(input_dir)

    # For each input Preset
    for preset in presets:

        # Opening files to work with
        # Default M1 Preset
        # Default M2 Preset
        # Input Preset
        # New Preset
        preset_file = input_dir/preset
        new_preset_file = preset_converted_dir/(os.path.basename(preset))
        with (
            open(default_m1_preset_file) as default_m1_preset,
            open(default_m2_preset_file) as default_m2_preset,
            open(preset_file) as old_preset,
            open(new_preset_file, 'w') as new_preset
        ):

            # Select default Preset
            if("speaker" in os.path.basename(preset).lower()):
                default_preset_xml = default_m2_preset.read().splitlines()
            else:
                default_preset_xml = default_m1_preset.read().splitlines()

            # Load old Preset
            old_preset_xml = old_preset.read().splitlines()

            # For each line of default Preset
            for default_line in default_preset_xml:
                default_line = default_line.strip()

                # # Keep Master Limiter & Playback Gain values to ViPER defaults

                # # Mode
                # # Master Switch -> Enabled
                # # Master Limiter (Output Pan) -> (50:50)
                # if any(key in default_line for key in ("32775", "36868", "65587")):
                #     if ("36868" in default_line):
                #         new_preset.write(default_line.replace("false", "true") + "\n")
                #     else:
                #         new_preset.write(default_line + "\n")

                # Mode
                # Master Limiter
                # Playback Gain Control
                if any(key in default_line for key in ("32775", "36868", "65586", "65587", "65588", "65565", "65566", "65567", "65568")):
                    # Master Switch -> Enabled
                    # Playback Gain -> Enabled
                    if (("36868" in default_line) or ("65565" in default_line)):
                        new_preset.write(default_line.replace("false", "true") + "\n")
                    else:
                        new_preset.write(default_line + "\n")

                # FET Compressor
                # ViPER DDC
                # Spectrum Extension
                # FIR Equalizer
                # Convolver
                # Field Surround
                # Headphone Surround +
                # Reverberation
                # Dynamic System
                # Tube Simulator (6N1J)
                # ViPER Bass
                # ViPER Clarity
                # Auditory System Protection
                # AnalogX
                # Speaker Optimization
                else:

                    # for each line of old Preset
                    for old_line in old_preset_xml:
                        old_line = old_line.strip()

                        # # Keep Master Limiter & Playback Gain values to ViPER defaults

                        # # Master Limiter

                        # if ("65586" in default_line):
                        #     if (("65586" in old_line) or ("65608" in old_line)):
                        #         old_line = old_line.split('"')
                        #         if 21 < int(old_line[3]) :
                        #             # Normalizing to range of 0 - 21
                        #             old_line[3] = str([1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200].index(int(old_line[3])))
                        #         old_line = '"'.join(old_line)
                        #         new_preset.write(old_line.replace("65608", "65586") + "\n")
                        #         break

                        # if ("65588" in default_line):
                        #     if (("65588" in old_line) or ("65609" in old_line)):
                        #         old_line = old_line.split('"')
                        #         if 5 < int(old_line[3]) :
                        #             # Normalizing to range of 0 - 5
                        #             old_line[3] = str([30, 50, 70, 80, 90, 100].index(int(old_line[3])))
                        #         old_line = '"'.join(old_line)
                        #         new_preset.write(old_line.replace("65609", "65588") + "\n")
                        #         break

                        # # Playback Gain Control

                        # if ("65565" in default_line):
                        #     if (("65565" in old_line) or ("65604" in old_line)):
                        #         new_preset.write(old_line.replace("65604", "65565") + "\n")
                        #         break

                        # if ("65566" in default_line):
                        #     if (("65566" in old_line) or ("65605" in old_line)):
                        #         old_line = old_line.split('"')
                        #         if 2 < int(old_line[3]) :
                        #             # Normalizing to range of 0 - 2
                        #             old_line[3] = str([50, 100, 300].index(int(old_line[3])))
                        #         old_line = '"'.join(old_line)
                        #         new_preset.write(old_line.replace("65605", "65566") + "\n")
                        #         break

                        # if ("65567" in default_line):
                        #     if (("65567" in old_line) or ("65606" in old_line)):
                        #         old_line = old_line.split('"')
                        #         if 5 < int(old_line[3]) :
                        #             # Normalizing to range of 0 - 5
                        #             old_line[3] = str([30, 50, 70, 80, 90, 100].index(int(old_line[3])))
                        #         old_line = '"'.join(old_line)
                        #         new_preset.write(old_line.replace("65606", "65567") + "\n")
                        #         break

                        # if ("65568" in default_line):
                        #     if (("65568" in old_line) or ("65607" in old_line)):
                        #         old_line = old_line.split('"')
                        #         if 10 < int(old_line[3]) :
                        #             # Normalizing to range of 0 - 10
                        #             old_line[3] = str([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000].index(int(old_line[3])))
                        #         old_line = '"'.join(old_line)
                        #         new_preset.write(old_line.replace("65607", "65568") + "\n")
                        #         break

                        # FET Compressor

                        if ("65610" in default_line):
                            if (("65610" in old_line) or ("65627" in old_line)):
                                new_preset.write(old_line.replace("65627", "65610") + "\n")
                                break

                        if ("65611" in default_line):
                            if (("65611" in old_line) or ("65628" in old_line)):
                                new_preset.write(old_line.replace("65628", "65611") + "\n")
                                break

                        if ("65612" in default_line):
                            if (("65612" in old_line) or ("65629" in old_line)):
                                new_preset.write(old_line.replace("65629", "65612") + "\n")
                                break

                        if ("65613" in default_line):
                            if (("65613" in old_line) or ("65630" in old_line)):
                                new_preset.write(old_line.replace("65630", "65613") + "\n")
                                break

                        if ("65614" in default_line):
                            if (("65614" in old_line) or ("65631" in old_line)):
                                new_preset.write(old_line.replace("65631", "65614") + "\n")
                                break

                        if ("65615" in default_line):
                            if (("65615" in old_line) or ("65632" in old_line)):
                                new_preset.write(old_line.replace("65632", "65615") + "\n")
                                break

                        if ("65616" in default_line):
                            if (("65616" in old_line) or ("65633" in old_line)):
                                new_preset.write(old_line.replace("65633", "65616") + "\n")
                                break

                        if ("65617" in default_line):
                            if (("65617" in old_line) or ("65634" in old_line)):
                                new_preset.write(old_line.replace("65634", "65617") + "\n")
                                break

                        if ("65618" in default_line):
                            if (("65618" in old_line) or ("65635" in old_line)):
                                new_preset.write(old_line.replace("65635", "65618") + "\n")
                                break

                        if ("65619" in default_line):
                            if (("65619" in old_line) or ("65636" in old_line)):
                                new_preset.write(old_line.replace("65636", "65619") + "\n")
                                break

                        if ("65620" in default_line):
                            if (("65620" in old_line) or ("65637" in old_line)):
                                new_preset.write(old_line.replace("65637", "65620") + "\n")
                                break

                        if ("65621" in default_line):
                            if (("65621" in old_line) or ("65638" in old_line)):
                                new_preset.write(old_line.replace("65638", "65621") + "\n")
                                break

                        if ("65622" in default_line):
                            if (("65622" in old_line) or ("65639" in old_line)):
                                new_preset.write(old_line.replace("65639", "65622") + "\n")
                                break

                        if ("65623" in default_line):
                            if (("65623" in old_line) or ("65640" in old_line)):
                                new_preset.write(old_line.replace("65640", "65623") + "\n")
                                break

                        if ("65624" in default_line):
                            if (("65624" in old_line) or ("65641" in old_line)):
                                new_preset.write(old_line.replace("65641", "65624") + "\n")
                                break

                        if ("65625" in default_line):
                            if (("65625" in old_line) or ("65642" in old_line)):
                                new_preset.write(old_line.replace("65642", "65625") + "\n")
                                break

                        if ("65626" in default_line):
                            if (("65626" in old_line) or ("65643" in old_line)):
                                new_preset.write(old_line.replace("65643", "65626") + "\n")
                                break

                        # FIR Equalizer

                        if ("65551" in default_line):
                            if (("65551" in old_line) or ("65595" in old_line)):
                                new_preset.write(old_line.replace("65595", "65551") + "\n")
                                break

                        if ("65552" in default_line):
                            if (("65552" in old_line) or ("65596" in old_line)):
                                new_preset.write(old_line.replace("65596", "65552") + "\n")
                                break

                        # Convolver

                        if ("65538" in default_line):
                            if (("65538" in old_line) or ("65589" in old_line)):
                                new_preset.write(old_line.replace("65589", "65538") + "\n")
                                break

                        if ("65540;65541;65542" in default_line):
                            if (("65540;65541;65542" in old_line) or ("65591;65592;65593" in old_line)):
                                # Correcting '&' in Kernel(.irs) names
                                old_line = old_line.replace("></string>amp;", "&amp;").replace(">Select impulse response file</string>amp;", "&amp;").replace("Select impulse response file", "").replace("Kernel", "").replace("Choose Impulse Response", "").replace("Selecione o arquivo de impulso de resposta", "")
                                new_preset.write(old_line.replace("65591;65592;65593", "65540;65541;65542") + "\n")
                                break

                        if ("65543" in default_line):
                            if (("65543" in old_line) or ("65594" in old_line)):
                                new_preset.write(old_line.replace("65594", "65543") + "\n")
                                break

                        # Reverberation

                        if ("65559" in default_line):
                            if (("65559" in old_line) or ("65597" in old_line)):
                                new_preset.write(old_line.replace("65597", "65559") + "\n")
                                break

                        if ("65560" in default_line):
                            if (("65560" in old_line) or ("65598" in old_line)):
                                old_line = old_line.split('"')
                                if 10 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 10
                                    old_line[3] = str(int(int(old_line[3])/10))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line.replace("65598", "65560") + "\n")
                                break

                        if ("65561" in default_line):
                            if (("65561" in old_line) or ("65599" in old_line)):
                                old_line = old_line.split('"')
                                if 10 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 10
                                    old_line[3] = str(int(int(old_line[3])/10))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line.replace("65599", "65561") + "\n")
                                break

                        if ("65562" in default_line):
                            if (("65562" in old_line) or ("65600" in old_line)):
                                new_preset.write(old_line.replace("65600", "65562") + "\n")
                                break

                        if ("65563" in default_line):
                            if (("65563" in old_line) or ("65601" in old_line)):
                                new_preset.write(old_line.replace("65601", "65563") + "\n")
                                break

                        if ("65564" in default_line):
                            if (("65564" in old_line) or ("65602" in old_line)):
                                new_preset.write(old_line.replace("65602", "65564") + "\n")
                                break

                        # ViPER DDC
                        # Spectrum Extention
                        # Field Surround
                        # Differential Surround
                        # Headphone Surround +
                        # Dynamic System
                        # Tube Simulator (6N1J)
                        # ViPER Bass
                        # ViPER Clarity
                        # Auditory System Protection
                        # AnalogX
                        if (default_line[default_line.find('"')+1:default_line.find('"', default_line.find('"')+1)] == old_line[old_line.find('"')+1:old_line.find('"', old_line.find('"')+1)]):

                            # Field Surround

                            if ("65554;65556" in default_line):
                                old_line = old_line.split('"')
                                if 8 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 8
                                    old_line[3] = str(int((int(old_line[3])-120)/10))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            if ("65555" in default_line):
                                old_line = old_line.split('"')
                                if 10 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 10
                                    old_line[3] = str(int((int(old_line[3])-120)/10))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            # Differential Surround

                            if ("65558" in default_line):
                                old_line = old_line.split('"')
                                if 19 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 19
                                    old_line[3] = str(int((int(old_line[3])/100)-1))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            # Dynamic System

                            if ("65573" in default_line):
                                old_line = old_line.split('"')
                                if 100 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 100
                                    old_line[3] = str(int((int(old_line[3])-100)/20))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            # ViPER Bass

                            if ("65576" in default_line):
                                old_line = old_line.split('"')
                                if 135 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 135
                                    old_line[3] = str(int(int(old_line[3])-15))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            if ("65577" in default_line):
                                old_line = old_line.split('"')
                                if 11 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 11
                                    old_line[3] = str(int((int(old_line[3])-50)/50))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            # ViPER Clarity

                            if ("65580" in default_line):
                                old_line = old_line.split('"')
                                if 9 < int(old_line[3]) :
                                    # Normalizing to range of 0 - 9
                                    old_line[3] = str(int(int(old_line[3])/50))
                                old_line = '"'.join(old_line)
                                new_preset.write(old_line + "\n")
                                break

                            # Remaining Features
                            new_preset.write(old_line + "\n")
                            break

                    # Speaker Optimization
                    else:
                        new_preset.write(default_line + "\n")

    return(preset_converted_dir)
