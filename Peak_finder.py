import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array
from pylab import *
import pandas as pd
from scipy import signal
import glob
import time
import os

'''
 Name:        Peak finder
 Purpose:     Straightforward function to find local min/max of 2D data

 Author:      Paul Sonda 
 Created:     7/31/2020
'''

def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    
    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.
    
    """
    maxtab = []   
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    #modify to have peak and trough as first two points
    
    maxtab.append((x[0], v[0]))
    mintab.append((x[1], v[1]))
    
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)
    
    
    
    # REAL Standardized peak mark,  try to compartmentalize it with optional input and images,  take out bins

def main():

# algorithm in pseudo-code

###################  1.  SET INPUTS:   PATH,  THRESHOLDS,  PARAMETERS #################################################
  
y1Thresh = 0.1  #for peak detect,  should be loose
y2Thresh = 1  # for peak detect, should be loose

mingain = 1 # capture all
maxphase = 99

butter_b, butter_a = signal.butter(3, 0.1)   #filter raw signal


evalDir = '..'
globFilter = 'file_name.csv'
dataType = 'Wave-C' #  can be drive,  electrical tester,  Wave-C, etc
tester = 'Wave-C'


# set bins where we will count peaks,  it is important to know if more than one peak in a bin

bins = {'GT1':{'rng': [5000,11000], 'mingain': 0.5, 'maxphase': 99, 'mingainprod': -1, 'color': 'yellow' },
    'GT2':{'rng': [11000,15500], 'mingain': 0.5, 'maxphase': 99, 'mingainprod': -1, 'color': 'grey'},
    'BP':{'rng': [15500,19500], 'mingain': 1, 'maxphase': 10, 'mingainprod': 3, 'color': 'yellow'},   #modify due to many 15 kHz
    '20kHz':{'rng': [19500,21000], 'mingain': 1, 'maxphase': 10, 'mingainprod': 3, 'color': 'white'},   
    'Sway':{'rng': [21000,27000], 'mingain': 1, 'maxphase': 10, 'mingainprod': 3, 'color': 'grey'},
    'GT4':{'rng': [27000,37000], 'mingain': 1, 'maxphase': 10, 'mingainprod': 3, 'color': 'yellow'},
    'Yaw':{'rng': [37000,43000], 'mingain': 3, 'maxphase': 10, 'mingainprod': 3, 'color': 'grey'},# Yaw modes should be big
    'Yaw2':{'rng': [43000,50000], 'mingain': 3, 'maxphase': 10, 'mingainprod': 3, 'color': 'yellow'}
   }

           
path = 'C:/Users/345341/Documents/DBT/'+evalDir


#############################   2.    READ INPUT FILE,  SET UP LOOPS   #############################

fil = path + globFilter
df = pd.read_csv(fil)

#  Generalize loop for different inputs,  could be just head_id,  could be drive serial number with multiple heads,  could be different radii/zht, etc

SNs = ['NA']  #  no drive serial number
hds = ['hd1', 'hd2','hd3'
trks = ['ID','OD']
zhts = ['nominal','low','high']    


############################   3.  LOOP THROUGH FILE,  CALL PEAK DETECT,  STORE SUMMARY DATA,   STORE IMAGES ##################

    
for SN in SNs:   #  step in unique identifiers
    for hd_index,hd in enumerate(hds):
        for trk in trks:
            for zht in zhts:
                
               # depending on different criteria,  data source,  filter out data to grab frequency,  gain, and phase         
               x = df.PEAK_FREQUENCY[filt]
               y1raw = df.GAIN[filt]
               y2raw = df.PHASE[filt]
                
               # filter noisy data
               y1=signal.filtfilt(butter_b,butter_a, y1raw)
               y2=signal.filtfilt(butter_b,butter_a, y2raw)

               #  CALL PEAK DETECT ALGORITHM - GAIN    
               maxtab,mintab = peakdet(y1,y1Thresh)
               
               peak_freqs = x[maxtab]
               peak_gains = y1[maxtab]
               
               # (not shown) a.  filter peaks based on bin, thresholds;   
               #  b.  calculate other criteria:  max peak per bin,  number of peaks per bin,  "pointiness" of peak,  etc.
               
               
               #  CALL PEAK DETECT ALGORITHM - GAIN    
               maxtab,mintab = peakdet(y1,y1Thresh)
               
               peak_freqs = x[maxtab]
               peak_gains = y1[maxtab]
               
               # (not shown) a.  filter peaks based on bin, thresholds;   
               #  b.  calculate other criteria:  max peak per bin,  number of peaks per bin,  "pointiness" of peak,  etc.
               
               
               detrended_phase = detrend(y2)  # optionally take out trend from phase plot
               
               #  CALL PEAK DETECT ALGORITHM - PHASE    
               maxtab,mintab = peakdet(y2,y2Thresh)
               
               peak_freqs_phase = x[mintab]
               peak_phases = y2[mintab]      

               # (not shown) a.  filter peaks based on bin, thresholds;   
               #  b.  calculate other criteria:  max peak per bin,  number of peaks per bin,  "pointiness" of peak,  etc.               
               
               
               
               # (not shown) Output data to summary csv files and create images   
