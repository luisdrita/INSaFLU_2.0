'''
Created on Oct 31, 2017

@author: mmp
'''
from .constants import Constants
from Bio import SeqIO
from django_q.tasks import fetch
from django.utils.translation import ugettext_lazy as _
from utils.result import CountHits
import os, random, gzip
import logging
from pysam import pysam

class Utils(object):
	'''
	class docs
	'''

	## logging
	logger_debug = logging.getLogger("fluWebVirus.debug")
	logger_production = logging.getLogger("fluWebVirus.production")

	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	def get_path_to_reference_file(self, user_id, ref_id):
		"""
		get the path to reference
		"""
		return os.path.join(Constants.DIR_PROCESSED_FILES_REFERENCE, "userId_{0}".format(user_id), "refId_{0}".format(ref_id))
	
	def get_path_to_fastq_file(self, user_id, sample_id):
		"""
		get the path to sample
		"""
		return os.path.join(Constants.DIR_PROCESSED_FILES_FASTQ, "userId_{0}".format(user_id), "sampleId_{0}".format(sample_id))

	def get_path_to_projec_file(self, user_id, project_id):
		"""
		get the path to project
		"""
		return os.path.join(Constants.DIR_PROCESSED_FILES_PROJECT, "userId_{0}".format(user_id), "projectId_{0}".format(project_id))
	
	def get_temp_file(self, file_name, sz_type):
		"""
		return a temp file name
		"""
		main_path = os.path.join(Constants.TEMP_DIRECTORY, Constants.COUNT_DNA_TEMP_DIRECTORY)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			return_file = os.path.join(main_path, "insa_flu_" + file_name + "_" + str(random.randrange(10000000, 99999999, 10)) + "_file" + sz_type)
			try:
				os.open(return_file, os.O_CREAT | os.O_EXCL)
				return return_file
			except FileExistsError:
				pass

	def get_temp_dir(self):
		"""
		return a temp directory
		"""
		main_path = os.path.join(Constants.TEMP_DIRECTORY, Constants.COUNT_DNA_TEMP_DIRECTORY)
		if (not os.path.exists(main_path)): os.makedirs(main_path)
		while 1:
			return_path = os.path.join(main_path, "insa_flu_" + str(random.randrange(10000000, 99999999, 10)))
			if (not os.path.exists(return_path)):
				os.makedirs(return_path)
				return return_path
	
	def get_file_name_without_extension(self, file_name):
		"""
		return file name without extension
		"""
		return os.path.splitext(os.path.basename(file_name))[0]
		
		
	def remove_temp_file(self, sz_file_name):
		"""
		prevent to remove files outside of temp directory
		"""
		if os.path.exists(sz_file_name) and len(sz_file_name) > 0 and sz_file_name.find(Constants.TEMP_DIRECTORY) == 0:
			cmd = "rm " + sz_file_name
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to remove a file") 

	def remove_dir(self, path_name):
		cmd = "rm -r %s*" % (path_name); os.system(cmd)

	def move_file(self, sz_file_from, sz_file_to):
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "mv " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to make a move a file") 
			
	def copy_file(self, sz_file_from, sz_file_to):
		if os.path.exists(sz_file_from):
			self.make_path(os.path.dirname(sz_file_to))
			cmd = "cp " + sz_file_from + " " + sz_file_to
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to make a move a file") 
			
	def make_path(self, path_name):
		if (not os.path.isdir(path_name) and not os.path.isfile(path_name)):
			cmd = "mkdir -p " + path_name
			os.system(cmd)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				self.logger_production.error('Fail to run: ' + cmd)
				self.logger_debug.error('Fail to run: ' + cmd)
				raise Exception("Fail to make a path") 
		
	def is_integer(self, n_value):
		try:
			int(n_value)
			return True
		except ValueError: 
			return False


	def is_float(self, n_value):
		try:
			float(n_value)
			return True
		except ValueError: 
			return False

	def is_gzip(self, file_name):
		"""
		test if the file name ends in gzip
		""" 
		return True if (file_name.rfind(".gz") == len(file_name) - 3) else False
	
	def is_fastq_gz(self, file_name):
		"""
		test if the file name ends in gzip
		raise Exception
		""" 
		if (not self.is_gzip(file_name)): raise Exception("File need to have suffix '.fastq.gz'")
		
		try:
			sz_type = self.get_type_file(file_name)
			if (sz_type == Constants.FORMAT_FASTQ): return True
		except OSError as e:
			self.logger_production.error("Fail to test '" + file_name + "' fastq.gz file: " + e.args[0])
			self.logger_debug.error("Fail to test '" + file_name + "' fastq.gz file: " + e.args[0])
		except Exception as e:
			self.logger_production.error("Fail to test '" + file_name + "' fastq.gz file: " + e.args[0])
			self.logger_debug.error("Fail to test '" + file_name + "' fastq.gz file: " + e.args[0])
		raise Exception("File is not in fastq.gz format")
		
	def get_type_file(self, file_name):
		"""
		return 'fasta' or 'fastq' 
		raise exception if can't detected
		"""
		if (self.is_gzip(file_name)): handle = gzip.open(file_name, mode='rt')	## need to be opened in text mode, default it's in binary mode
		else: handle = open(file_name)
		for record in SeqIO.parse(handle, Constants.FORMAT_FASTQ):
			handle.close() 
			return Constants.FORMAT_FASTQ
		handle.close()
		
		if (self.is_gzip(file_name)): handle = gzip.open(file_name, mode='rt')
		else: handle = open(file_name)
		for record in SeqIO.parse(handle, Constants.FORMAT_FASTA):
			handle.close() 
			return Constants.FORMAT_FASTA
		handle.close()
		
		raise Exception("Can't detect file format for the file '" + file_name + "'")
	

	def is_fasta(self, sz_file_name):
		"""
		Test Fata file
		"""
		handle = open(sz_file_name)
		b_pass = False
		for line in handle:
			sz_temp = line.strip()
			if (len(sz_temp) == 0): continue
			if (sz_temp[0] == ">"): 
				b_pass = True
				break
			else: 
				handle.close()
				raise IOError(_("Error: the file is not in FASTA format."))
		handle.close()
		if (not b_pass): raise IOError(_("Error: the file is not in FASTA format."))

		record_dict = SeqIO.index(sz_file_name, "fasta")
		if (len(record_dict) > 0): return len(record_dict)
		raise IOError(_("Error: the file is not in FASTA format."))

	
	def is_genbank(self, sz_file_name):
		"""
		Test GenBank file
		"""
		handle = open(sz_file_name)
		b_pass = False
		for line in handle:
			sz_temp = line.strip()
			if (len(sz_temp) == 0): continue
			if (sz_temp.startswith("LOCUS", 0)): 
				b_pass = True
				break
			else: 
				handle.close()
				raise IOError(_("Error: the file is not in GenBank format."))
		handle.close()
		if (not b_pass): raise IOError(_("Error: the file is not in GenBank format."))

		n_number_locus = 0
		for record in SeqIO.parse(sz_file_name, "genbank"):
			n_number_locus += 1
		if (n_number_locus > 0): return n_number_locus
		raise IOError(_("Error: the file is not in GenBank format."))


	def read_text_file(self, file_name):
		"""
		read text file and put the result in an vector
		"""
		if (not os.path.exists(file_name)):
			self.logger_production.error("Fail to read '" + file_name)
			self.logger_debug.error("Fail to test '" + file_name)
			raise IOError(_("Error: file '" + file_name + "' doens't exist."))
		
		vect_out = []
		handle = open(file_name)
		for line in handle:
			sz_temp = line.strip()
			if (len(sz_temp) == 0): continue
			vect_out.append(sz_temp)
		handle.close()
		return vect_out
	
	def compare_locus_fasta_gb(self, fasta_file, gb_file):
		"""
		Test if all fasta locus are in gb file
		"""
		locus_fasta = self.is_fasta(fasta_file)
		locus_gb = self.is_genbank(gb_file)
		if (locus_gb != locus_fasta): raise ValueError(_("Number of locus are different from fasta to genbank."))
		
		record_dict = SeqIO.index(fasta_file, "fasta")
		try:
			for record in SeqIO.parse(gb_file, "genbank"):
				b_found = False
				for seq in record_dict:
					if (seq == record.name):
						if (len(record_dict[seq].seq) != len(record.seq)):
							raise ValueError(_("Different length. Fasta seq: %s length: %d; Fasta seq: %s length: %d." 
										% (seq, len(record_dict[seq].seq), record.name, len(record.seq))) )
						b_found = True
						break
				if (not b_found): raise ValueError(_("This locus '" + record.name + "' is not in fasta file."))
		except AttributeError as e:
			raise ValueError(_(e.args[0]))
		return locus_fasta


	def get_all_files(self, directory):
		"""
		return all files from a directory
		"""
		return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


	def compress_files(self, software, file_name):
		"""
		compress files
		"""
		## test if the file exists
		if (os.path.exists(file_name + ".gz")): return
		
		cmd = "{} -c {} > {}.gz".format(software, file_name, file_name)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.logger_production.error('Fail to run: ' + cmd)
			self.logger_debug.error('Fail to run: ' + cmd)
			raise Exception("Fail to compress file") 

	def create_index_files(self, software, file_name):
		"""
		create index, need to be .gz
		"""
		file_to_index = file_name
		if (not file_to_index.endswith(".gz")): file_to_index += ".gz"
		if (not os.path.exists(file_to_index)):
			self.logger_production.error("File doesn't exist: " + file_to_index)
			self.logger_debug.error("Fail doesn't exist: " + file_to_index)
			raise Exception("File doesn't exist")
		
		## test if tbi exists
		if (os.path.exists(file_to_index + '.tbi')): return

		cmd = "{} {}".format(software, file_name)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			self.logger_production.error('Fail to run: ' + cmd)
			self.logger_debug.error('Fail to run: ' + cmd)
			raise Exception("Fail to create index") 
	
	def str2bool(self, v):
		"""
		str to bool
		"""
		return v.lower() in ("yes", "true", "t", "1")
		
	def is_all_tasks_finished(self, vect_tasks_id):
		"""
		return true if all tasks finished
		"""
		for task_id in vect_tasks_id:
			task = fetch(task_id)
			if (task == None): return False
		return True

	def is_all_tasks_finished_success(self, vect_tasks_id):
		"""
		return true if all tasks finished
		"""
		for task_id in vect_tasks_id:
			task = fetch(task_id)
			if (task == None): continue
			if (not task.success): return False
		return True


	def add_freq_to_vcf(self, vcf_file, vcf_file_out):
		"""
		add FREQ to VCF, FREQ=AO/DP
		vcffile must be gzip and tbi included
		"""
		FREQ = 'FREQ'
		
		#read the input file
		vcf_hanlder = pysam.VariantFile(vcf_file, "r")
		if (FREQ in vcf_hanlder.header.info): 
			vcf_hanlder.close()
			return
		
		vcf_hanlder_write = pysam.VariantFile(vcf_file_out, "w")
		vcf_hanlder.header.info.add(FREQ, number='A', type='Float', description='Ratio of AO/DP')

		## write the header
		for variant_header_records in vcf_hanlder.header.records:
			vcf_hanlder_write.header.add_record(variant_header_records)
		
		for variant_sample in vcf_hanlder.header.samples:
			vcf_hanlder_write.header.add_sample(variant_sample)
			
		for variant in vcf_hanlder:
			if ("DP" in variant.info and "AO" in variant.info):
				vect_ao_out = []
				for value_ in variant.info['AO']:
					vect_ao_out.append((value_/float(variant.info['DP']) * 100))
				variant.info[FREQ] = tuple(vect_ao_out)
			vcf_hanlder_write.write(variant)
			
		vcf_hanlder_write.close()
		vcf_hanlder.close()
		return vcf_file_out


	def count_hits_from_tab(self, tab_file):
		"""
		NP	864	snp	G	T	99.6855	CDS	+	864/1497	288/498	synonymous_variant c.864G>T p.Gly288Gly	locus_00005		Nucleoprotein
		count the hits by <50; 50-90
		"""
		count_hits = CountHits()
		with open(tab_file) as handle:
			for line in handle:
				sz_temp = line.strip()
				if (len(sz_temp) == 0 or sz_temp[0] == '#'): continue
				lst_data = sz_temp.split('\t')
				if (len(lst_data) > 5):
					freq_data = lst_data[5]
					for value_ in freq_data.split(','):
						if (self.is_float(value_)):
							if (float(value_) < 50): count_hits.add_one_hits_less_50()
							elif (float(value_) < 91): count_hits.add_one_hits_50_90()
		return count_hits



				


