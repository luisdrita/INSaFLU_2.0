'''
Created on Nov 1, 2017

@author: mmp
'''
from managing_files.models import MetaKeySample, MetaKey, MetaKeyProject, MetaKeyProjectSample, MetaKeyReference
from managing_files.models import CountVariations, Statistics, TagName, ProjectSample
from constants.tag_names_constants import TagNamesConstants
from constants.meta_key_and_values import MetaKeyAndValue
from django.db import connection

class ManageDatabase(object):
	'''
	classdocs
	'''
	def __init__(self):
		'''
		Constructor
		'''
		pass
	def set_reference_metakey(self, reference, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		try:
			metaKey = MetaKey.objects.get(name=meta_key_name)
		except MetaKey.DoesNotExist:
			metaKey = MetaKey()
			metaKey.name = meta_key_name
			metaKey.save()
		
		metaKeyReference = MetaKeyReference()
		metaKeyReference.reference = reference
		metaKeyReference.meta_tag = metaKey
		metaKeyReference.owner = owner
		metaKeyReference.value = value
		metaKeyReference.description = description
		metaKeyReference.save()
		return metaKeyReference
	
	def get_reference_metakey(self, reference, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyReference.objects.filter(reference__id=reference.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyReference.objects.get(reference__id=reference.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyReference.DoesNotExist:
			return None
	
	def get_reference_metakey_last(self, reference, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyReference.objects.filter(reference__id=reference.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyReference.objects.filter(reference__id=reference.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyReference.DoesNotExist:
			return None	
		
	
	def set_sample_metakey(self, sample, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		try:
			metaKey = MetaKey.objects.get(name=meta_key_name)
		except MetaKey.DoesNotExist:
			metaKey = MetaKey()
			metaKey.name = meta_key_name
			metaKey.save()
		
		metaKeySample = MetaKeySample()
		metaKeySample.sample = sample
		metaKeySample.meta_tag = metaKey
		metaKeySample.owner = owner
		metaKeySample.value = value
		metaKeySample.description = description
		metaKeySample.save()
		return metaKeySample
	
	def get_sample_metakey(self, sample, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeySample.objects.filter(sample__id=sample.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeySample.objects.get(sample__id=sample.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeySample.DoesNotExist:
			return None
	
	def get_sample_metakey_last(self, sample, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeySample.objects.filter(sample__id=sample.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeySample.objects.filter(sample__id=sample.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeySample.DoesNotExist:
			return None	
		
	def set_project_metakey(self, project, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		try:
			metaKey = MetaKey.objects.get(name=meta_key_name)
		except MetaKey.DoesNotExist:
			metaKey = MetaKey()
			metaKey.name = meta_key_name
			metaKey.save()
		
		metaKeyProject = MetaKeyProject()
		metaKeyProject.project = project
		metaKeyProject.meta_tag = metaKey
		metaKeyProject.owner = owner
		metaKeyProject.value = value
		metaKeyProject.description = description
		metaKeyProject.save()
		return MetaKeyProject
	
	def get_project_metakey(self, project, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyProject.objects.filter(project__id=project.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyProject.objects.get(project__id=project.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyProject.DoesNotExist:
			return None
		
	def get_project_metakey_last(self, project, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyProject.objects.filter(project__id=project.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyProject.objects.filter(project__id=project.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyProject.DoesNotExist:
			return None	

	def set_project_sample_metakey(self, project_sample, owner, meta_key_name, value, description):
		"""
		save a meta key
		"""
		try:
			metaKey = MetaKey.objects.get(name=meta_key_name)
		except MetaKey.DoesNotExist:
			metaKey = MetaKey()
			metaKey.name = meta_key_name
			metaKey.save()
		
		metaKeyProjectSample = MetaKeyProjectSample()
		metaKeyProjectSample.project_sample = project_sample
		metaKeyProjectSample.meta_tag = metaKey
		metaKeyProjectSample.owner = owner
		metaKeyProjectSample.value = value
		metaKeyProjectSample.description = description
		metaKeyProjectSample.save()
		return metaKeyProjectSample
	
	def get_project_sample_metakey(self, project_sample, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): return MetaKeyProjectSample.objects.filter(project_sample__id=project_sample.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			return MetaKeyProjectSample.objects.get(project_sample__id=project_sample.id, meta_tag__name=meta_key_name, value=value)
		except MetaKeyProjectSample.DoesNotExist:
			return None

	def get_project_sample_metakey_last(self, project_sample, meta_key_name, value):
		"""
		value = None, return a list
		"""
		try:
			if (value == None): query_set = MetaKeyProjectSample.objects.filter(project_sample__id=project_sample.id, meta_tag__name=meta_key_name).order_by('-creation_date')
			else: query_set = MetaKeyProjectSample.objects.filter(project_sample__id=project_sample.id, meta_tag__name=meta_key_name, value=value).order_by('-creation_date')
			if (query_set.count() > 0 ): return query_set[0]
			return None
		except MetaKeyProject.DoesNotExist:
			return None	

	def get_project_sample_starts_with_metakey(self, project_sample, meta_key_name):
		"""
		in: meta_key_name + '%'
		return a list with match
		"""
		try:
			return list(MetaKeyProjectSample.objects.filter(project_sample__id=project_sample.id, meta_tag__name__startswith=meta_key_name).order_by('-creation_date'))
		except MetaKeyProject.DoesNotExist:
			return []	


	def get_variation_count(self, count_hits):
		"""
		Add values in project_sample
		"""
		if (count_hits == None): return None
		
		count_variations = CountVariations()
		count_variations.var_bigger_50_90 = count_hits.get_hits_50_90()
		count_variations.var_bigger_90 = count_hits.get_hits_more_90()
		count_variations.var_less_50 = count_hits.get_hits_less_50()
		count_variations.total = count_hits.get_total()
		count_variations.save()
		return count_variations


	#######################################
	###
	###		deal with percentils
	###

	
	def percentils_refresh(self, user):
		"""
		refresh the percentils
		"""
		## don't calc the percentils
		if (CountVariations.objects.count() < TagNamesConstants.MINIMUM_NUMBER_TO_COUNT_STATISTICS): return
		
		tagNamesConstants = TagNamesConstants()
		for percentil_tag in tagNamesConstants.get_all_tags_percentil():
			try: 
				statistics = Statistics.objects.get(tag__name=percentil_tag)
			except Statistics.DoesNotExist:
				
				try:
					tag_name = TagName.objects.get(name=percentil_tag, owner__id=user.id)
				except TagName.DoesNotExist:
					tag_name = TagName()
					tag_name.name = percentil_tag
					tag_name.owner = user
					tag_name.is_meta_data = tagNamesConstants.is_meta_tag_name(percentil_tag)
					tag_name.save()
				
				statistics = Statistics()
				statistics.tag = tag_name
			
			### set the values
			percentil_value = self.get_percentil_value(percentil_tag)
			if (percentil_value != None):
				statistics.value = percentil_value
				statistics.save()
	
	
	def set_percentis_alert(self, project_sample, user, count_hits, percentil_name):
		"""
		in: percentil_name from tagNamesConstants.get_percentil_tag_name(TagNamesConstants.TAG_PERCENTIL_95, TagNamesConstants.TAG_PERCENTIL_VAR_TOTAL), or other
		return True if has an alert
		"""
		tagNamesConstants = TagNamesConstants()
		
		### get the percentil for total
		percentil_value = self.get_percentil_value_from_db(percentil_name)
		if (percentil_value != None):
			b_percentil_fault = False
			if (percentil_name.endswith(TagNamesConstants.TAG_PERCENTIL_VAR_TOTAL) and count_hits.get_total() > percentil_value): b_percentil_fault = True
			elif (percentil_name.endswith(TagNamesConstants.TAG_PERCENTIL_VAR_50) and count_hits.get_hits_less_50() > percentil_value): b_percentil_fault = True
			elif (percentil_name.endswith(TagNamesConstants.TAG_PERCENTIL_VAR_50_90) and count_hits.get_hits_50_90() > percentil_value): b_percentil_fault = True
			
			if (b_percentil_fault):
				### set the alert
				project_sample = ProjectSample.objects.get(pk=project_sample.id)
				project_sample.alert_first_level += 1
				project_sample.save()
				self.set_project_sample_metakey(project_sample, user, MetaKeyAndValue.META_KEY_ALERT_COUNT_VAR,\
								MetaKeyAndValue.META_VALUE_Error,\
								"Warning, this sample has a total of variations '{}' bigger than the percentile {} of all database".\
								format(count_hits.get_total(), int(tagNamesConstants.get_number_percentil_from_tag(percentil_name))))
			return True
		return False


	def get_percentil_value(self, percentil_name):
		"""
		in: percentil_name from tagNamesConstants.get_percentil_tag_name(TagNamesConstants.TAG_PERCENTIL_95, TagNamesConstants.TAG_PERCENTIL_VAR_TOTAL)
		return  the float percentil value from database
		
		select total_matched, ntile(100) over (order by total_matched), cume_dist() OVER (ORDER BY total_matched) as percentile from runner;

		select avg(total_matched) from (select total_matched, ntile(100) over (order by total_matched), cume_dist() OVER (ORDER BY total_matched) as percentile from market_book) where ntile = 99;
		select avg(total_matched) from (select total_matched, ntile(100) over (order by total_matched), cume_dist() OVER (ORDER BY total_matched) as percentile from market_book) ss where ntile = 99;
		select avg(total) from (select total, ntile(100) over (order by total), cume_dist() OVER (ORDER BY  total) as percentile from managing_files_countvariations) ss where ntile = 99;
		"""
		## get the percentil float to get the value, 97.5, 95, 90, or other
		tagNamesConstants = TagNamesConstants()
		percentil_float = tagNamesConstants.get_number_percentil_from_tag(percentil_name)
		
		if (CountVariations.objects.count() < TagNamesConstants.MINIMUM_NUMBER_TO_COUNT_STATISTICS):
			return tagNamesConstants.get_emperical_percentil_values(percentil_float)
		
		## calculate for total
		cursor = connection.cursor()
		if (tagNamesConstants.is_which_var(percentil_name, TagNamesConstants.TAG_PERCENTIL_VAR_TOTAL)):
			cursor.execute('select avg(total) from (select total, ntile(100) over (order by total), cume_dist() OVER (ORDER BY total)' +\
					' as percentile from managing_files_countvariations) ss where ntile = {};'.format(percentil_float))
		elif (tagNamesConstants.is_which_var(percentil_name, TagNamesConstants.TAG_PERCENTIL_VAR_50)):
			cursor.execute('select avg(var_less_50) from (select var_less_50, ntile(100) over (order by var_less_50), cume_dist() OVER (ORDER BY var_less_50)' +\
					' as percentile from managing_files_countvariations) ss where ntile = {};'.format(percentil_float))
		elif (tagNamesConstants.is_which_var(percentil_name, TagNamesConstants.TAG_PERCENTIL_VAR_50_90)):
			cursor.execute('select avg(var_bigger_50) from (select var_bigger_50, ntile(100) over (order by var_bigger_50), cume_dist() OVER (ORDER BY var_bigger_50)' +\
					' as percentile from managing_files_countvariations) ss where ntile = {};'.format(percentil_float))
		row = cursor.fetchall()
		if (row != None and len(row) > 0 and len(row[0]) > 0): return int(row[0][0])
		return None


	def get_percentil_value_from_db(self, percentil_tag):
		"""
		get the statistic that is in database
		return None if not exist 
		"""
		try: 
			statistics = Statistics.objects.get(tag__name=percentil_tag)
			return statistics.value
		except Statistics.DoesNotExist:
			pass
		return None
		
	###
	###		END deal with percentils
	###
	#######################################
	
	
		