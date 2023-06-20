import sys
sys.path.insert(0, "/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration")
import numpy as np
from utils import *
from cam2_read_area_draw_fig import read_csv_draw


# y为peak_height area, x为depth, reflectance = area * (depth^2) * k --> area = k * reflectance/(depth^2) 
def calc_k(x1, x2, y1, y2):  
    x = np.array(list(x1)+list(x2))  # reflectance/(depth^2)
    y = np.array(list(y1) + list(y2))  # area
    sorted_tuples = sorted(zip(x, y))
    x = np.array([t[0] for t in sorted_tuples])
    y = np.array([t[1] for t in sorted_tuples])
    k = y/x
    return np.var(k)


def calc_xy(csv_path, power_num):
    depth_area_list = read_csv_draw(csv_path) 
    depth_list = depth_area_list[:,0] # [depth_high_single, area_high_1burst, area_high_4burst, area_low_1burst, area_low_4burst] 
    area_high_1burst = depth_area_list[:,1]  # area_s
    area_high_4burst = depth_area_list[:,2]  # area_s
    area_low_1burst = depth_area_list[:,3]  # area_s
    area_low_4burst = depth_area_list[:,4]  # area_s
    tmp_x = depth_list ** power_num  # (depth**α)
    return tmp_x, [area_high_1burst, area_high_4burst, area_low_1burst, area_low_4burst]
  
    
if __name__ == "__main__":
    ref_1 = 0.2
    ref_2 = 0.9
    power_range = range(-5, 5)
    k_var = []
    for power_tmp in power_range:
        # ------------------------
        # 20%
        csv1_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_area_20%_all.csv"
        tmp_x1, y1 = calc_xy(csv1_path, power_tmp)
        y1 = y1[0]
        
        # ------------------------
        # 90%
        csv2_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_area_90%_all.csv"
        tmp_x2, y2 = calc_xy(csv2_path, power_tmp)
        y2 = y2[0]
        
        # ------------------------ 
        least_k_loss_sum = 999999999
        k_loss = []
        t_r = []
        for i in np.linspace(ref_1-0.1, ref_1+0.1, 20):
            for j in np.linspace(ref_2-0.1, ref_2+0.1, 20):
                x1 = i/tmp_x1  
                x2 = j/tmp_x2 
                k_const=calc_k(x1, x2, y1, y2)
                k_loss.append(k_const)
                if least_k_loss_sum>k_const:
                    least_k_loss_sum = k_const
        print("least_k_var =", least_k_loss_sum, "; when_power=", power_tmp)
        draw_pic(x=range(len(k_loss)), y=k_loss, xlabel="times", ylabel="K_var", title="power="+str(power_tmp))
        k_var.append(least_k_loss_sum)
    draw_pic(x=power_range, y=k_var, xlabel="power_range", ylabel="K_var", title="k_var to power")