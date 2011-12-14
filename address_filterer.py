#!/bin/python

import csv
import os
from glob import glob

THIS_FILE = os.path.abspath(__file__)
THIS_DIR = os.path.split(THIS_FILE)[0]
OUTFILE = THIS_DIR + "\\results.csv"

def main(files):
	print "\n### %s ###\n" % __file__

	addresses = addresses_from_files(files)
	print "Total addresses: %d\n" % len(addresses)

	addresses = without_invalid(addresses, ('zip', 'city'))
	print "Without invalid: %d\n" % len(addresses)

	addresses = without_duplicates(addresses, ('address1', 'zip'))
	print "Without duplicates: %d\n" % len(addresses)

	write_addresses(addresses)
	print "Data written to: \n%s" % OUTFILE

def addresses_from_files(files):
	addresses = []
	clean_address = dict_kv_mapper(clean_text)
	for file in files:
		print "Reading file: %s" % file.split("\\")[-1]
		addresses += [clean_address(address) for address in csv.DictReader( open(file) )]

	return addresses

def without_invalid(data, validation_keys):
	print "Validating addresses . . ."
	print "Validation keys: %s" % str(validation_keys)

	return [address for address in data if valid_address(address, validation_keys)]

def without_duplicates(data, duplication_keys):
	print "Filtering duplicates . . ."
	print "Duplication signature: %s" % str(duplication_keys)

	return signature_filter(data, address_signaturizer(duplication_keys))

def write_addresses(data, outfile=OUTFILE):
	with open(outfile, "wb") as file:
		writer = csv.DictWriter(file, data[0].keys(), extrasaction='ignore')
		writer.writeheader()
		writer.writerows(data)

def dict_kv_mapper(f):
	def kv_map(dict):
		for k, v in dict.items():
			dict[k] = f(k, v)
		return dict

	return kv_map

def clean_text(key, text):
	text = text.replace('.', '').replace("  ", ' ').upper().strip(" ")

	if key == 'address1':
		if text.endswith(' ST'):
			text = text[:-2] + 'STREET'
		elif text.endswith(' RD'):
			text = text[:-2] + "ROAD"
		elif text.endswith(' AV') or text.endswith(" AVE"):
			text = ' '.join(text.split(' ')[:-1]) + " AVENUE"
		elif text.endswith(' PL'):
			text = text[:-2] + "PLACE"
		elif text.endswith(' WY'):
			text = text[:-2] + "WAY"

	if key == 'zip':
		text = text.split('-')[0]

	return text

def valid_address(address, valid_keys):
	for k in valid_keys:
		if not address[k]:
			return False

	c = address['country']
	if c != 'US' and c != 'USA' and c != '':
		return False
	if not address['zip'].isdigit():
		return False

	return True

def signature_filter(collection, signaturize=lambda x: x):
	# Credit: Alex Martelli - http://www.peterbe.com/plog/uniqifiers-benchmark
	signatures = {}
	results = []
	for item in collection:
		sig = signaturize(item)
		if sig not in signatures:
			signatures[sig] = True
			results.append(item)

	return results

def address_signaturizer(signature_keys):
	def signaturize(address):
		return tuple([v for k, v in address.items() if k in signature_keys])

	return signaturize


if __name__ == "__main__":
	main( glob( os.path.join( THIS_DIR + "\\data\\", '*.csv' ) ) )
