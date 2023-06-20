import pylab
import numpy as np
from utils import *


# y为peak_height area, x为depth, reflectance = area * (depth^2) * k --> area = k * reflectance/(depth^2) 
def calc_k(x1, x2, x3, y1, y2, y3):  
    x = np.array(list(x1)+list(x2)+list(x3))  # reflectance/(depth^2)
    y = np.array(list(y1) + list(y2) + list(y3))  # area
    sorted_tuples = sorted(zip(x, y))
    x = np.array([t[0] for t in sorted_tuples])
    y = np.array([t[1] for t in sorted_tuples])
    k = y/x
    return np.var(k)

def calc_xy(reflectance, csv_path, power_num):
    depth_area = open_csv_to_array(csv_path)
    depth_list = depth_area[:,0]
    area_list = depth_area[:,1]  # area_s
    x = reflectance/(depth_list ** power_num)  # reflectance/(depth^2)
    return x, area_list
    
if __name__ == "__main__":
    ref_1 = 0.2
    ref_2 = 0.52
    ref_3 = 0.9
    power_range = range(-5, 5)
    k_var = []
    for power_tmp in power_range:
        # 20%
        csv_path = r"/home/zhangyouan/桌面/zya/TOF/611/peak_height_area_20%_18.csv"
        x1, y1 = calc_xy(ref_1, csv_path, power_tmp)
        
        # ------------------------
        # 52%
        csv_path = r"/home/zhangyouan/桌面/zya/TOF/611/peak_height_area_52%_18.csv"
        x2, y2 = calc_xy(ref_2, csv_path, power_tmp)
        
        # ------------------------ 
        # 90%
        csv_path = r"/home/zhangyouan/桌面/zya/TOF/611/peak_height_area_90%_18.csv"
        x3, y3 = calc_xy(ref_3, csv_path, power_tmp)
        
        # ------------------------ 
        least_k_loss_sum = 999999999
        k_loss = []
        for i in np.linspace(ref_1-0.1, ref_1+0.1, 20):
            for j in np.linspace(ref_2-0.1, ref_2+0.1, 20):
                for k in np.linspace(ref_3-0.1, ref_3+0.1, 20):
                    y1 = i/x1
                    y2 = j/x2
                    y3 = k/x3
                    k_const=calc_k(x1, x2, x3, y1, y2, y3)
                    k_loss.append(k_const)
                    if least_k_loss_sum>k_const:
                        least_k_loss_sum = k_const
        print("least_k_var =", least_k_loss_sum, "; when_power=", power_tmp)
        draw_pic(x=range(len(k_loss)), y=k_loss, xlabel="times", ylabel="K_var", title="power="+str(power_tmp))
        k_var.append(least_k_loss_sum)
    draw_pic(x=power_range, y=k_var, xlabel="power_range", ylabel="K_var", title="k_var to power")