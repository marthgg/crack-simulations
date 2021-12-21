# Packages
import numpy as np
import matplotlib.pyplot as plt
import os

from scipy.optimize import curve_fit

from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *

# Packages form Henriks Github
from lammps_logfile import running_mean, get_color_value
from regex_file_collector import Collector
from regex_file_collector.utils import floating_number_pattern
import lammps_logfile

# Sigmoidal function
def sigmoid(x, c, b, a):
    z = b*(x-c)
    return a*np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))

# Path to files
path = '/home/users/marthgg/2021_10_change_pressureX/'
pattern = 'crack_simulation_'+floating_number_pattern('pressX')+'/trajectory.bin'

collection = Collector(path, pattern, fields=('pressX'))
simulations = collection.get_flat()

# Find crack tip position
def trajectory_to_fracture_displacement(filename, reference_frame=7):
    
    # Read in trajectory-file
    pipeline = import_file(filename, multiple_frames=True)

    position_crack_tip = []
    frames = []
    frames_posCrack = []
    
    extra_zeros = np.zeros((50))

    for frame in range(reference_frame, pipeline.source.num_frames):
        
        # Coordination analysis:
        pipeline.modifiers.append(CoordinationAnalysisModifier(cutoff = 2.1, number_of_bins = 10, partial = True))
        
        # Select type (oxygen atoms):
        pipeline.modifiers.append(SelectTypeModifier(types = {1}))

        # Expression selection:
        pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'Coordination >=2'))

        # Delete selected:
        pipeline.modifiers.append(DeleteSelectedModifier())

        # Spatial binning:
        pipeline.modifiers.append(SpatialBinningModifier(property = 'Coordination', reduction_operation = SpatialBinningModifier.Operation.Sum, 
                                                         direction = SpatialBinningModifier.Direction.X, bin_count = (200, 200, 200)))
        

        #Extract and save data as a table
        data = pipeline.compute(frame)
        table = data.tables['binning'].xy()

        pos_x = table[:,0]
        coord = table[:,1]

        diff_pos = pos_x[1]-pos_x[0]

        # Add extra zeroes at the end to get a better fit
        new_pos = []
        for i in range (0, len(extra_zeros)):
            new_pos.append(pos_x[-1]+diff_pos*i)

        pos_x = np.insert(pos_x, len(pos_x), new_pos)
        coord = np.insert(coord, len(coord), extra_zeros)

        # Make a sigmoidal fit (for x3000_y200: 500)
        popt = [200]

        try:
            popt, pcov = curve_fit(sigmoid, pos_x, coord, p0=[popt[0], 0.001, (pos_x[0]+pos_x[-1])/2])
        except RuntimeError as e: 
            print(e)
            popt = [-1]
            
        #plt.figure()
        #plt.plot(pos_x, coord, label='data')
        #plt.plot(sig_x, sig_y, label='fit')
        #plt.legend()
        #plt.show()
                
        position_crack_tip.append(popt[0])
        
    return position_crack_tip

# Function to save as .npy-file
def save_fracture_displacement(filename, overwrite=True, **kwargs):
    outfile = "fracture_displacement"
    
    folder = os.path.dirname(filename)
    
    if overwrite or not os.path.isfile(os.path.join(folder, outfile+".npy")):
        position_crack_tip = trajectory_to_fracture_displacement(filename, **kwargs)
        np.save(os.path.join(folder,outfile), position_crack_tip, allow_pickle=False)
        
# Create and save .npy-files
for deformZ, path in simulations.items():
   
    filename = path
    print(filename)
    
    save_fracture_displacement(filename)