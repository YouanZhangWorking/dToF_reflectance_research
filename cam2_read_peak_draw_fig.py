import numpy as np
from utils import *


def read_peak_csv_draw(csv_path, display=False):
    depth_peak = open_area_to_list(csv_path)
    
    depth_high_tmp = depth_peak[::2][:,0]
    depth_high_list = np.array(list(float(i[0:-1]) for i in depth_high_tmp))
    peak_high_list = np.array(list(map(float, depth_peak[::2][:,2])))
    depth_high_list_single = depth_high_list[::2]
    peak_high_list_1burst = peak_high_list[::2]
    peak_high_list_4burst = peak_high_list[1::2]
    
    depth_low_tmp = depth_peak[1::2][:,0]
    depth_low_list = np.array(list(float(i[0:-1]) for i in depth_low_tmp))
    peak_low_list = np.array(list(map(float, depth_peak[1::2][:,2])))
    depth_low_list_single = depth_low_list[::2]
    peak_low_list_1burst = peak_low_list[::2]
    peak_low_list_4burst = peak_low_list[1::2]
    
    if display == True:
        draw_pic(depth_high_list_single, peak_high_list_1burst, xlabel="depth", ylabel="peak", title="High_1burst")
        draw_pic(depth_high_list_single, peak_high_list_4burst, xlabel="depth", ylabel="peak", title="High_4burst")
        draw_pic(depth_low_list_single, peak_high_list_1burst, xlabel="depth", ylabel="peak", title="Low_1burst")
        draw_pic(depth_low_list_single, peak_high_list_4burst, xlabel="depth", ylabel="peak", title="Low_4burst")
        fig = pylab.figure()
        plot1 = pylab.plot(depth_high_list_single, peak_high_list_1burst, "g")
        plot2 = pylab.plot(depth_high_list_single, peak_high_list_4burst, "o")
        plot3 = pylab.plot(depth_high_list_single, peak_low_list_1burst,"r")
        plot4 = pylab.plot(depth_high_list_single, peak_low_list_4burst,"*")
        pylab.legend(labels=["1high","4high", "1low", "4low"])
        pylab.xlabel("depth")
        pylab.ylabel("peak")
        pylab.show()
    
    return np.array([depth_high_list_single[4:], 
                     peak_high_list_1burst[4:], peak_high_list_4burst[4:], 
                     peak_low_list_1burst[4:], peak_low_list_4burst[4:]])
    
if __name__ == "__main__":
    csv_20_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_20%_all.csv"
    csv_90_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_90%_all.csv"
    peak_20_dif_module = read_peak_csv_draw(csv_path=csv_20_path)
    peak_90_dif_module = read_peak_csv_draw(csv_path=csv_90_path)
    