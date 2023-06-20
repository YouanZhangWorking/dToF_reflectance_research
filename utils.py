import csv
import os
import sys
import numpy as np
import pylab
import matplotlib.pyplot as plt


# 1. 读取csv,并返回csv数值，为二维数组
def open_csv_to_array(file_name):
    result = []
    csv_reader = csv.reader(open(file_name))
    for line in csv_reader:
        line = np.array([float(i) for i in line])
        result.append(line)
    result_numpy = np.array(result)
    return result_numpy

def open_area_to_list(file_name):
    result = []
    csv_reader = csv.reader(open(file_name))
    for line in csv_reader:
        line[2] = float(line[2])
        result.append(line)
    result_numpy = np.array(result)
    return result_numpy
        

# 2. 绘图
def draw_pic(x, y, xlabel="reflectance/(depth^2)", ylabel="area", title="Pic"):
    fig = pylab.figure()
    plot1 = pylab.plot(x, y, 'r')
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.show()
    
    
# 3. 读取二维数组，并在同一张图上进行绘制
def array_to_hist(xy_arrays, x_label, y_label, title, xlim=None, ylim=None):
    line, column = xy_arrays.shape
    print(line, column)
    fig, ax = plt.subplots()  # 创建图实例
    for i, key in enumerate(xy_arrays):
        x = range(column)
        ax.plot(x, key)
    if xlim != None:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim != None:
        ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label) 
    ax.set_title(title) 
    ax.legend()
    plt.show()  
    
    
# 4. 查找子目录的所有文件的目录名
def find_all_sub_folder_name(folder_path):
    name_list = os.listdir(folder_path)
    return name_list


# 5. 从csv读取数据，左右找pixel height,然后计算梯形面积，求和得到peak height面积；
def find_highest_peak_height_area(hist_path): # hist_csv_path
    hist_array = open_csv_to_array(hist_path)  # 对于每一行数据
    area_all_pixel = []
    for key_i in hist_array: # 对于每一个pixel的historgm,计算peak height area;
        key_i = list(key_i)
        tmp_peak = max(key_i)
        tmp_peak_idx = key_i.index(tmp_peak)
        
        # 最大值的前一个非零索引
        before_val_idx = next((i for i in range(tmp_peak_idx-1, -1, -1) if key_i[i] != 0), None)
        if before_val_idx == None:
            before_val_idx = tmp_peak_idx
        # 最大值的后一个非零索引
        after_val_idx = next((i for i in range(tmp_peak_idx+1, len(key_i)) if key_i[i] != 0), None)
        if after_val_idx == None:
            after_val_idx = tmp_peak_idx
            
        # 计算peak height area
        area_peak = 0
        for m in range(before_val_idx, after_val_idx):
            left_h = key_i[m]
            right_h = key_i[m+1]
            area_tmp = (left_h+right_h)*1/2
            area_peak += area_tmp
        area_all_pixel.append(area_peak)  # 统计每一个pixel的area;
        # print(len(area_all_pixel))
    # print(np.shape(area_all_pixel))
    return area_all_pixel  # shape = (576,)


# 5.1 从csv读取数据，左右找pixel height,然后peak*1,使用长方形，求和得到peak height面积；
def find_highest_peak_height_rect_area(hist_path): # hist_csv_path
    hist_array = open_csv_to_array(hist_path)  # 对于每一行数据
    area_all_pixel = []
    for key_i in hist_array: # 对于每一个pixel的historgm,计算peak height area;
        key_i = list(key_i)
        tmp_peak = max(key_i)
        tmp_peak_idx = key_i.index(tmp_peak)
        
        # 最大值的前一个非零索引
        before_val_idx = next((i for i in range(tmp_peak_idx-1, -1, -1) if key_i[i] != 0), None)
        if before_val_idx == None:
            before_val_idx = tmp_peak_idx
        # 最大值的后一个非零索引
        after_val_idx = next((i for i in range(tmp_peak_idx+1, len(key_i)) if key_i[i] != 0), None)
        if after_val_idx == None:
            after_val_idx = tmp_peak_idx
            
        # 计算peak height area
        area_peak = 0
        for m in range(before_val_idx, after_val_idx+1):
            height = key_i[m]
            area_tmp = height*1
            area_peak += area_tmp
        area_all_pixel.append(area_peak)  # 统计每一个pixel的area;
        # print(len(area_all_pixel))
    # print(np.shape(area_all_pixel))
    return area_all_pixel  # shape = (576,)

# 5.2 从csv读取数据，max之后，根据左右阈值，找thresh rate；
def find_highest_peak_height_thresh_area(hist_path, threshrate): # hist_csv_path
    hist_array = open_csv_to_array(hist_path)  # 对于每一行数据
    area_all_pixel = []
    for key_i in hist_array: # 对于每一个pixel的historgm,计算peak height area;
        key_i = list(key_i)
        tmp_peak = max(key_i)
        tmp_peak_idx = key_i.index(tmp_peak)
        thresh = threshrate*tmp_peak
        
        # 最大值的前一个非零索引
        before_val_idx = next((i for i in range(tmp_peak_idx-1, -1, -1) if key_i[i] > thresh), None)
        if before_val_idx == None:
            before_val_idx = tmp_peak_idx
        # 最大值的后一个非零索引
        after_val_idx = next((i for i in range(tmp_peak_idx+1, len(key_i)) if key_i[i] > thresh), None)
        if after_val_idx == None:
            after_val_idx = tmp_peak_idx
            
        # 计算peak height area
        area_peak = 0
        for m in range(before_val_idx, after_val_idx):            
            left_h = key_i[m]
            right_h = key_i[m+1]
            area_tmp = (left_h+right_h)*1/2
            area_peak += area_tmp
            
        area_all_pixel.append(area_peak)  # 统计每一个pixel的area;
        # print(len(area_all_pixel))
    # print(np.shape(area_all_pixel))
    return area_all_pixel  # shape = (576,)
        
        
# 6. 选则中间正方形部分为wall
def find_wall_peak_area(all_peak_height_area, center_size=1):  # (576, 0)
    '''
      pixel顺序:
        575 574 .  ... 552  
        .   .   .      .
        .   .   .      .
        .   .   .      24
        23  22  21 ... 0
      area顺序;
        [0,1,2...575]
      center_size:1, 3, 5, ...
    '''
    all_peak_height_area = all_peak_height_area[::-1]  # 倒叙
    all_peak_height_area = np.array(all_peak_height_area)  
    all_peak_height_area = all_peak_height_area.reshape((24, 24))  # 变成实际pixel顺序
    tmp_left = (24-1)//2-(center_size//2) #2: 10
    tmp_right = (24-1)//2+(center_size//2) # 2: 13
    
    mid_values_avg = np.mean(all_peak_height_area[tmp_left:tmp_right, tmp_left:tmp_right])
    # if tmp_left == tmp_right:
    #   mid_values = [all_peak_height_area[tmp_left][tmp_right]]
    # elif tmp_left < tmp_right:
    #   mid_values = [all_peak_height_area[i][j] for i in range(tmp_left, tmp_right) for j in range(tmp_left, tmp_right)]
    # # print(tmp_left, tmp_right)
    # # print(all_peak_height_area[11][11])
    
    # # 计算mid value的均值；
    # mid_values_avg = np.mean(mid_values)
    
    return mid_values_avg
    # center_idx 
    

# 6. 将arr写入csv
def write2csv(arr, file_path):
    # 1. 创建文件对象
    f = open(file_path, 'w', encoding='utf-8')
    
    # 2. 基于文件对象构建csv写入对象
    csv_writer = csv.writer(f, delimiter=',')
    
    # 3. 构建列表头
    # csv_writer.writerow(("depth", "peak_area"))
    for i in arr:   
        csv_writer.writerow(i)
    
    # 5. 关闭文件
    f.close()
    
    

# 7. 绘制图像
def draw_pic(x, y, xlabel="reflectance/(depth^2)", ylabel="area", title="Pic", fig=True):
    if fig == True:
        fig = pylab.figure()
        plot1 = pylab.plot(x, y, 'r')
        pylab.title(title)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.show()
    else:
        plot1 = pylab.plot(x, y, 'r')
        pylab.xlabel(xlabel)