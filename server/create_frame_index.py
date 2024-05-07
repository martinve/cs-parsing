#!/usr/bin/env python3
"""
Create a human-readable website listing the given frames.
"""

__author__ = "Skatje Myers"
__license__ = "CC-BY-SA-4.0"

import argparse
import os
import re
import sys
from pathlib import Path
from lxml import etree as ET


def main(frame_dir):
	# Read and extract frame info
	frame_files = frame_dir.rglob('*.xml')
	frames = dict()
	for frame_file in frame_files:
		try:
			xml = ET.parse(str(frame_file))
			frames[frame_file.name] = xml
		except Exception:
			pass  # TODO: If the XML can't be parsed, we're just ignoring the file. Should handle this better.
	website_title = 'PropBank Frames'

	all_rolesets = get_rolesets(frames)
	resources, roleset_to_resource_use = read_usagenotes(frames)
	alias_word_to_rolesets = get_aliases_to_rolesets(frames)

	print("All rolesets:", len(all_rolesets))
	print("Aliases:", len(alias_word_to_rolesets))

	import pprint
	# pprint.pprint(alias_word_to_rolesets, indent=2)

	# pprint.pprint(alias_word_to_roleset	roleset_pred_map, aliases = get_resource_maps(alias_word_to_rolesets, all_rolesets, roleset_to_resource_use)

	roleset_pred_map, aliases = get_resource_maps(alias_word_to_rolesets, all_rolesets, roleset_to_resource_use)

	for it in roleset_pred_map:
		print(it[0], "\t", it[1], sep="")



def get_rolesets(frames):
	all_rolesets = dict()
	for frame_name, xml in frames.items():
		rs = [e.get('id') for e in xml.findall('predicate/roleset')]
		for id in rs:
			all_rolesets[id] = frame_name[:-4]
	return all_rolesets


def read_usagenotes(frames):
	resources = set()
	roleset_to_resource_use = dict()
	for frame_name, xml in frames.items():
		resource_names = [e.get('resource') + '_' + e.get('version').replace('.', '-').replace(' ', '_') for e in xml.findall('predicate/roleset/usagenotes/usage')]
		rs = xml.findall('predicate/roleset')
		for roleset in rs:
			usages = [e.get('resource') + '_' + e.get('version').replace('.', '-').replace(' ', '_') for e in roleset.findall('usagenotes/usage') if e.get('inuse') == '+']
			roleset_to_resource_use[roleset.get('id')] = usages
		resources.update(resource_names)
	resources = list(resources)
	resources = sorted(resources)
	return resources, roleset_to_resource_use


def get_aliases_to_rolesets(frames):
	alias_word_to_rolesets = dict()
	for frame_name, xml in frames.items():
		for roleset in xml.findall('predicate/roleset'):
			aliases = roleset.find('aliases')
			if aliases is None:
				continue
			aliases = aliases.findall('alias')
			for alias in aliases:
				if '\n' in alias.text:
					print('')
				if alias.text not in alias_word_to_rolesets:
					alias_word_to_rolesets[alias.text] = [roleset]
				else:
					alias_word_to_rolesets[alias.text].append(roleset)
	for alias, rolesets in alias_word_to_rolesets.items():
		rolesets.sort(key=lambda x: x.get('id'))
	return alias_word_to_rolesets


def get_resource_maps(alias_word_to_rolesets, all_rolesets, roleset_to_resource_use):

	# Alias to resources:
	aliases = {}
	for alias, rolesets in alias_word_to_rolesets.items():
		alias_resources = set()
		for roleset in rolesets:
			alias_resources.update(roleset_to_resource_use[roleset.get('id')])
	aliases.update({alias: alias_resources})

	# Roleset search functions:
	roleset_pred_map = all_rolesets.items()
	# print("Roleset predicate map", len(roleset_pred_map), list(roleset_pred_map)[:10])

	k = 0
	for x in roleset_pred_map:
		if "zoom" in x:
			# print(x[0], x[1])
			k += 1
		if k > 10: break

	# Alias search functions:
	aliases = alias_word_to_rolesets.keys()
	# print("Aliases", len(aliases), list(aliases)[:10])
	for x in alias_word_to_rolesets:

		if "zoom" in x:
			# print(x)
			# print(x)
			k += 1
		if k > 10: break


	return roleset_pred_map, aliases


if __name__ == "__main__":

	fpath = "/home/martin/nltk_data/propbank-frames/frames"
	input_frames = Path(fpath)

	print(input_frames)
	assert input_frames.exists()


	"""
	for frame_file in input_frames.rglob('*.xml'):
		found_errors = validate(frame_file, Path(website_dir, 'frame_errors.txt'))  # TODO: We should have it spit out the errors to a file, then make them accessible via HTML
		need_error_warning = need_error_warning or found_errors
	"""


	main(input_frames)
