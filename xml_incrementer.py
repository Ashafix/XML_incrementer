from copy import deepcopy
import sys
import xml.etree.ElementTree as ET

help_message = """
Usage: python xml_incrementer.py xml-file start stop steps
       e.g. python xml_incrementer.py woo.xml 0 1 50
       Your output file will be named new_woo.xml"""

def main(filename, start, stop, steps):

    old_xml = ET.parse(filename)
    new_xml = deepcopy(old_xml)

    #find where the value is stored
    tags = ['Presets', 'Preset', 'Controls', 'ValueControl']
    element = old_xml.getroot().find(tags[0])
    for tag in tags[1:]:
        element = element.find(tag)
        if not element:
            print('error: not all elements could be found')
            sys.exit()
        if tag == 'Preset':
            preset = element

    #overwrite first value
    element.attrib['value'] = str(start)

    #create new elements and change value
    step_size = float(stop - start) / steps
    for i in range(1, steps + 1):
        new_xml.find(tags[0]).append(deepcopy(preset))
        element.attrib['value'] = str(i * step_size)

    #write to new file
    new_xml.write('new_{}'.format(filename))

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(help_message)
        sys.exit()
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))