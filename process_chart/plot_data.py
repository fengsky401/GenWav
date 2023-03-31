import matplotlib.pyplot as plt

# 定义横坐标和纵坐标数据
x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
y = [0, 0, 0, 0, 18, 19, 9, 16, 16, 20, 7, 20, 11, 12, 3, 0, 0, 0, 3, 3, 0]

# 绘制柱状图
plt.bar(x, y, width=0.05, edgecolor='white')

# 添加横坐标和纵坐标的标签
plt.xlabel('Value', fontsize=12)
plt.ylabel('Frequency')

# 设置横坐标的刻度，并设置字体大小
plt.xticks(x, fontsize=8)


# 显示图像
plt.show()