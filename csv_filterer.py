import csv
import os
from glob import glob

THIS_FILE = os.path.abspath(__file__)
THIS_DIR = os.path.split(THIS_FILE)[0]
OUTFILE = THIS_DIR + "\\results.csv"

def main(files):
	print "\n### %s ###\n" % __file__
	
	csv_data = csv_from_files(files)
	print "Total addresses: %d\n" % len(csv_data)
	
	csv_data = without_invalid(csv_data, ('zip', 'city'))
	print "Without invalid: %d\n" % len(csv_data)
	
	csv_data = without_duplicates(csv_data, ('address1', 'zip'))
	print "Without duplicates: %d\n" % len(csv_data)
	
	write_data(csv_data)
	print "Data written to: \n%s" % OUTFILE
	
def csv_from_files(files):
	csv_data = []
	clean_dict = dict_kv_mapper(clean_text)
	for file in files:
		print "Reading file: %s" % file.split("\\")[-1]
		data = [clean_dict(dict) for dict in csv.DictReader( open(file) )]
		csv_data += data
		
	return csv_data
	
def without_invalid(data, validation_keys):
	print "Validating addresses . . ."
	print "Validation keys: %s" % str(validation_keys)
	
	return [dict for dict in data if valid_dict(dict, validation_keys)]
	
def without_duplicates(data, duplication_keys):
	print "Filtering duplicates . . ."
	print "Duplication signature: %s" % str(duplication_keys)
	
	return signature_filter(data, dict_signaturizer(duplication_keys))
		
def write_data(data, outfile=OUTFILE):
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

def valid_dict(dict, valid_keys):
	for k in valid_keys:
		if not dict[k]:
			return False
			
	c = dict['country']
	if c != 'US' and c != 'USA' and c != '':
		return False
	if not dict['zip'].isdigit():
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

def dict_signaturizer(signature_keys):
	def signature(dict):
		return tuple([v for k, v in dict.items() if k in signature_keys])
		
	return signature
	
	
if __name__ == "__main__":
	main( glob( os.path.join( THIS_DIR + "\\data\\", '*.csv' ) ) )