from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def get_dowy(dt):
	'''Converts Pandas DateTimeIndex Timestamp to day of water year.

	Parameters
	----------
	dt : timestamp
		Pandas DateTimeIndex Timestamp.

	Returns
	-------
	dowy : int
		Day of Water Year, the number of days since the first day of the current water year.
	'''
	
	dt = datetime(dt.year,dt.month,dt.day)

	year = dt.year
	if (dt-datetime(year,9,30)).days > 0:
		strtYear = year
	else:
		strtYear = year-1
		
	return (dt - datetime(strtYear,9,30)).days

def get_wy(dt):
	'''Converts Pandas DateTimeIndex Timestamp to water year.

	Parameters
	----------
	dt : timestamp
		Pandas DateTimeIndex Timestamp.

	Returns
	-------
	wy : int
		Water year of the supplied timestamp.
	'''
	
	dt = datetime(dt.year,dt.month,dt.day)
	
	year = dt.year
	
	if (dt-datetime(year,9,30)).days > 0:
		wy = year + 1
	else:
		wy = year
		
	return wy

def get_smWY(dt):
	'''Converts Pandas DateTimeIndex Timestamp to a snowmodel water year.

	Parameters
	----------
	dt : timestamp
		Pandas DateTimeIndex Timestamp.

	Returns
	-------
	wy : int
		Water year of the supplied timestamp.
	'''
	
	dt = datetime(dt.year,dt.month,dt.day)
	
	year = dt.year
	
	if (dt-datetime(year,8,31)).days > 0:
		wy = year + 1
	else:
		wy = year
		
	return wy

def get_mowy(dt):
	'''Coverts Pandas DateTimeIndex Timestamp to month of water year.

	Parameters
	----------
	dt : timestamp
		Pandas DateTimeIndex Timestamp

	Returns
	-------
	wy : int
		Month of the water year from the supplied timestamp.
	'''

	dt = datetime(dt.year,dt.month,dt.day)

	year = dt.year
	month = dt.month

	if (dt-datetime(year,9,30)).days > 0:
		month = month - 9
	else:
		month = month + 3
		
	return month

def standardize(var):
	'''Standardize a variable by subtracting the mean and dividing by the standard deviation.

	Parameters
	----------
	var : np.array
		The variable to standardize.

	Returns
	-------
	standVar : np.array
		The standardized variable.
	'''

	return (var - np.mean(var))/np.std(var)

def Lstandardize(var):
	'''Standardize a variable by subtracting the mean and dividing by the standard deviation using L-moments.

	Parameters
	----------
	var : np.array
		The variable to standardize.

	Returns
	-------
	standVar : np.array
		The standardized variable.
	'''
	import lmoments3 as lm

	mean,std = lm.lmom_ratios(var,nmom = 2)

	return (var-mean)/std

def get_decimal_year(dt):
	'''Convert Pandas DateTimeIndex to a decimal year.

	Parameters
	----------
	dt : Timestamp
		Pandas DateTimeIndex Timestamp.

	Returns
	-------
	dy : float
		Decimal year of the supplied timestamp.
	'''

	dt = datetime(dt.year,dt.month,dt.day)

	year = dt.year

	start_of_year = datetime(year,1,1)

	end_of_year = datetime(year,12,31)

	days = (end_of_year-start_of_year).days + 1

	doy = (dt-start_of_year).days

	return year+float(doy)/float(days)

def traceFromOutlet(outlet,nhru):
	'''Trace upstream from a HUC.
	
	Parameters
	----------
	outlet : str
		Textual code for the input HUC.

	Returns
	-------
	hrus : list
		List of HUC or HRU codes for upstream hydrologic units.
	'''
	upstreams = list(nhru.loc[nhru.ToHUC == outlet].HUC12.values) # get the upstream hucs
	n = len(upstreams)

	hrus = []
	hrus.append(outlet)
	n = len(upstreams)
	while n > 0:
		newUpstreams = []
		for upstream in upstreams:
			hrus.append(upstream) # track all the HRUs processed
			newUpstreams.extend(list(nhru.loc[nhru.ToHUC == upstream].HUC12.values)) # grow the list

		n = len(newUpstreams)
		upstreams = newUpstreams
		
	return hrus

def plot_network(outlet,nhru,nseg):
	'''Plot upstream hydrologic units

	Parameters
	----------
	outlet : str
		Textual code of the outlet huc to trace upstream from.

	Returns
	-------
	None
	'''

	hrus = traceFromOutlet(outlet)
	segment = nhru.loc[nhru.HUC12 == outlet].hru_id.values[0].astype('int').astype('str')
	segIDs = list(nhru[nhru.HUC12.isin(hrus)].hru_segmen.values)
	ax = nhru[nhru.HUC12.isin(hrus)].plot(color = 'g', alpha = 0.5, edgecolor='0.2', figsize = (8,6)) # plot HRUs
	nhru[nhru.HUC12.isin([outlet])].plot(color='0.5', ax = ax, edgecolor = '0.2')
	nseg[nseg.seg_id.isin(segIDs)].plot(ax=ax, color='r')
	plt.title('Segment: %s'%segment)