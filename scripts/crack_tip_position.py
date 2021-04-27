# Packages
from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

from regex_file_collector import Collector
from regex_file_collector.utils import floating_number_pattern

def sigmoid(x, c, b, a):
    z = b*(x-c)
    return a*np.where(z >= 0, 1 / (1 + np.exp(-z)), np.exp(z) / (1 + np.exp(z)))

# Path to files

path = '/home/users/marthgg/simulations/change_deformZ/'
pattern = 'crack_simulation_'+floating_number_pattern('deformZ')+'/trajectory.bin'

collection = Collector(path, pattern, fields=('deformZ'))
simulations = collection.get_flat()

counter = 0

for deformZ, path in simulations.items():
    #counter += 1
    #if counter > 2:
    #    break
    file_name = path
    print(file_name)
    pipeline = import_file(file_name, multiple_frames=True)

    position_crack_tip = []
    frames = []

    extra_zeros = np.zeros((20))

    #inital guess
    popt = [100]

    for frame in range(7, pipeline.source.num_frames):
        # Coordination analysis:
        pipeline.modifiers.append(CoordinationAnalysisModifier(number_of_bins = 10, partial = True))

        # Expression selection:
        pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'Coordination>=4 || ParticleType==2'))

        # Delete selected:
        pipeline.modifiers.append(DeleteSelectedModifier())

        # Spatial binning:
        pipeline.modifiers.append(SpatialBinningModifier(property = 'Coordination', reduction_operation = SpatialBinningModifier.Operation.Sum, direction = SpatialBinningModifier.Direction.X, bin_count = (95, 200, 200)))

        data = pipeline.compute(frame)

        table = data.tables['binning'].xy()

        pos_x = table[:,0]
        coord = table[:,1]

        diff_pos = pos_x[1]-pos_x[0]

        new_pos = []
        for i in range (0, len(extra_zeros)):
            new_pos.append(pos_x[-1]+diff_pos*i)

        pos_x = np.insert(pos_x, len(pos_x), new_pos)
        coord = np.insert(coord, len(coord), extra_zeros)

        popt = [100]

        try:
            popt, pcov = curve_fit(sigmoid, pos_x, coord, p0=[popt[0], 0.001, (pos_x[0]+pos_x[-1])/2])
        except RuntimeError as e: 
            print(e)
            popt = [-1]
        
        #print(popt)
        position_crack_tip.append(popt[0])
        frames.append(frame)

        if popt[0] < 0:
            print('Remove negative value')
            position_crack_tip.pop(-1)
            frames.pop(-1)
        
        if (popt[0] > pos_x[-1]) or (popt[0]<100):
            print('Value out of area')
            position_crack_tip.pop(-1)
            frames.pop(-1)
            
        #sig_x = np.linspace(pos_x[0], pos_x[-1], len(pos_x))
        #sig_y = sigmoid(sig_x, *popt)

        #plt.figure()
        #plt.plot(pos_x, coord, label='data')
        #plt.plot(sig_x, sig_y, label='fit')
        #plt.legend()
        #plt.show()

        # Plot crack tip position with frame
        #velocity = []
        #for i in range(0, len(frames)):
        #    velocity.append(position_crack_tip[i]/frames[i])
    
    plt.figure(1)
    plt.plot(frames, position_crack_tip, label=deformZ)
    plt.xlabel('Frames')
    plt.ylabel('Position x')
    plt.ylim([0, 1000])
    plt.legend()

plt.show()
