import numpy as np
from utils import *


def read_csv_draw(csv_path, display=False):
    depth_area = open_area_to_list(csv_path)
    depth_high_tmp = depth_area[::2][:,0]
    depth_high_list = np.array(list(float(i[0:-1]) for i in depth_high_tmp))
    area_high_list = np.array(list(map(float, depth_area[::2][:,2])))
    # print(depth_high_list)
    # print(area_high_list)
    depth_high_list_single = depth_high_list[::2]
    area_high_list_1burst = area_high_list[::2]
    area_high_list_4burst = area_high_list[1::2]
    
    depth_low_tmp = depth_area[1::2][:,0]
    depth_low_list = np.array(list(float(i[0:-1]) for i in depth_low_tmp))
    area_low_list = np.array(list(map(float, depth_area[1::2][:,2])))
    # print(depth_low_list)
    # print(area_low_list)
    depth_low_list_single = depth_low_list[::2]
    area_low_list_1burst = area_low_list[::2]
    area_low_list_4burst = area_low_list[1::2]
    
    if display == True:
        draw_pic(depth_high_list_single, area_high_list_1burst, xlabel="depth", ylabel="area", title="High_1burst")
        draw_pic(depth_high_list_single, area_high_list_4burst, xlabel="depth", ylabel="area", title="High_4burst")
        draw_pic(depth_low_list_single, area_high_list_1burst, xlabel="depth", ylabel="area", title="Low_1burst")
        draw_pic(depth_low_list_single, area_high_list_4burst, xlabel="depth", ylabel="area", title="Low_4burst")
        fig = pylab.figure()
        plot1 = pylab.plot(depth_high_list_single, area_high_list_1burst, "g")
        plot2 = pylab.plot(depth_high_list_single, area_high_list_4burst, "o")
        plot3 = pylab.plot(depth_high_list_single, area_low_list_1burst,"r")
        plot4 = pylab.plot(depth_high_list_single, area_low_list_4burst,"*")
        pylab.legend(labels=["1high","4high", "1low", "4low"])
        pylab.xlabel("depth")
        pylab.ylabel("area")
        pylab.show()
    
    return np.array([depth_high_list_single[4:], 
                     area_high_list_1burst[4:], area_high_list_4burst[4:], 
                     area_low_list_1burst[4:], area_low_list_4burst[4:]])
    
if __name__ == "__main__":
    csv_20_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_area_20%_all.csv"
    csv_90_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_area_90%_all.csv"
    area_20_dif_module = read_csv_draw(csv_path=csv_20_path)
    area_90_dif_module = read_csv_draw(csv_path=csv_90_path)
    