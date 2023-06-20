import numpy as np
from cam2_read_area_draw_fig import read_csv_draw
from utils import draw_pic
import pylab

def try_poly(x, y, power_num=1):
    z = np.polyfit(x, y, power_num)
    p1 = np.poly1d(z)
    return p1


# (Ref) / dis = F(Area)
def polyfit_area(csv_path, ref, module=0):
    depth_area = read_csv_draw(csv_path)
    depth = depth_area[0]
    area = depth_area[module+1] # module=0,1,2,3 ["1high", "4high", "1low", "4low"]
    formula_area = try_poly(area, ref/(depth**2), power_num=2)
    y_truth = ref/(depth**2)
    y_pred = formula_area(area)
    loss = abs(y_truth-y_pred)
    print(loss)
    plot1 = pylab.plot(depth, y_truth, '*', label='original values')
    plot2 = pylab.plot(depth, y_pred, 'r', label='fit values')
    pylab.show()

# (dis**2) * area
def show_dis_square_area(csv_path, module=0):
    depth_area = read_csv_draw(csv_path)
    depth = depth_area[0]
    module_list = ["1high", "4high", "1low", "4low"]
    area = depth_area[module+1] # module=0,1,2,3 ["1high", "4high", "1low", "4low"]
    y = area * (depth**2)
    x = depth
    draw_pic(x, y, xlabel="depth", ylabel="area*depth^2", title=module_list[module])    


if __name__ == "__main__":
    csv20_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_area_20%_all.csv" 
    csv90_path = r"/home/zhangyouan/桌面/zya/TOF/611/test1_area_ref_exploration/peak_height_area_90%_all.csv"
    
    polyfit_area(csv20_path, 1, 0)
    # polyfit_area(csv90_path, 0.9, 0)