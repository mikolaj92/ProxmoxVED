#!/usr/bin/env python3
import xml.etree.ElementTree as ET

# Read XML
tree = ET.parse('/config/data/root/default/TV Shows/options.xml')
root = tree.getroot()

# Find PathInfos element
path_infos = root.find('PathInfos')

# Replace it with new content
new_path_infos = ET.fromstring('''<PathInfos>
    <PathInfo>
      <Path>/root/arr-stack/media/tv</Path>
    </PathInfo>
  </PathInfos>'')

# Remove old and add new
if path_infos is not None:
    root.remove(path_infos)
root.append(new_path_infos)

# Write back
tree.write('/config/data/root/default/TV Shows/options.xml', encoding='utf-8', xml_declaration=True)

print("Updated TV Shows options.xml")

# Also do Movies
tree2 = ET.parse('/config/data/root/default/Movies/options.xml')
root2 = tree2.getroot()

path_infos2 = root2.find('PathInfos')
new_path_infos2 = ET.fromstring('''<PathInfos>
    <PathInfo>
      <Path>/root/arr-stack/media/movies</Path>
    </PathInfo>
  </PathInfos>''')

if path_infos2 is not None:
    root2.remove(path_infos2)
root2.append(new_path_infos2)

tree2.write('/config/data/root/default/Movies/options.xml', encoding='utf-8', xml_declaration=True)

print("Updated Movies options.xml")
