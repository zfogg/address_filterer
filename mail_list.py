import csv
import os
from glob import glob

THIS_FILE = os.path.abspath(__file__)
THIS_DIR = os.path.split(THIS_FILE)[0]
PARENT_DIR = os.path.split(THIS_DIR)[0]

def main(files):
	print "\n\t###\n"
	csv_data = csv_from_files(files)
	print "\n\n\tTotal addresses: %d\n" % len(csv_data)
	csv_data = without_invalid(csv_data)
	print "Without invalid: %d\n" % len(csv_data)
	csv_data = without_duplicates(csv_data)
	print "Without duplicates: %d\n" % len(csv_data)
	write_data(csv_data)
	
def csv_from_files(files):
	csv_data = []
	for file in files:
		print "Reading file: %s" % file.split("\\")[-1]
		data = [clean_dict(dict) for dict in csv.DictReader(open(file))]
		csv_data += data
	return csv_data
	
def without_invalid(data):
	print "Validating addresses . . ."
	valid_keys = ('zip', 'city')
	print "Validation keys: %s" % str(valid_keys)
	return [dict for dict in data if valid_dict(dict, valid_keys)]
	
def without_duplicates(data):
	print "Filtering duplicates . . ."
	unique_keys = ('address1', 'zip')
	print "Duplication signature: %s" % str(unique_keys)
	return f5_filter( [x for x in data], address_signature(unique_keys) )
		
def write_data(data):
	with open(PARENT_DIR + "\\results.csv", "wb") as f:
		writer = csv.DictWriter(f, data[0].keys(), extrasaction='ignore')
		writer.writeheader()
		writer.writerows(data)

def valid_dict(dict, valid_keys):
	for k in valid_keys:
		if not dict[k]: return False
		
	c = dict['country']
	if c != 'US' and c != 'USA' and c != '':
		return False
	if not dict['zip'].isdigit():
		return False
	
	return True

def address_signature(unique_keys):
	def f(address):
		signature = []
		for k, v in address.items():
			if k in unique_keys:
				signature.append(v)
		return tuple(signature)
	return f
	
def f5_filter(seq, idfun=lambda x: x):
	seen = {}
	result = []
	for item in seq:
		marker = idfun(item)
		if marker in seen: continue
		seen[marker] = 1
		result.append(item)
	return result
		
def clean_dict(dict):
	def clean(text, key):
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
		if key == 'zip':
			text = text.split('-')[0]
		return text
		
	for k, v in dict.items():
		dict[k] = clean(dict[k], k)
	return dict
	
if __name__ == "__main__":
	main( glob( os.path.join( PARENT_DIR + "\\data\\", '*.csv' ) ) )