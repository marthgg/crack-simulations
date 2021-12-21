def findVelocity(filename, timestep, dump_frequency):
    data = np.load(filename, allow_pickle=False)
    frames = list(range(0, len(data)))
    
    filtered_data_crackTip = []
    filtered_data_frames   = []
    
    for i in range(0, len(data)):
        if data[i] > crack_start_point and data[i] < system_length:
            filtered_data_crackTip.append(data[i])
            filtered_data_frames.append(frames[i])
            
    for i in range(0, len(filtered_data_frames)):
        if filtered_data_crackTip[i] > 2910:
            print(filename)
            print(filtered_data_frames[i])
            break
            
    # Find velocity
    timestep = timestep # ps
    dump_frequency = dump_frequency

    time_s = []
    time = []
    for i in range(0, len(filtered_data_frames)):
        time.append(filtered_data_frames[i]*timestep*dump_frequency) #Time in ps
        if filtered_data_crackTip[i] < 2910:
            time_s.append(filtered_data_frames[i]*timestep*dump_frequency*(10**-12)) #time in s

    position_m = []
    for i in range(0, len(filtered_data_crackTip)):
        if filtered_data_crackTip[i] < 2910:
            position_m.append(filtered_data_crackTip[i]*(10**-10)) #distance in m
            
    velocity = np.diff(position_m)/np.diff(time_s)
    mean_velocity = np.mean(velocity)
    
    return mean_velocity