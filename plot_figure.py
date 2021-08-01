from matplotlib import pyplot as plt
import numpy as np
from numpy.core.function_base import linspace
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# best & farthest
x = np.array([i+1 for i in range(14)])
y = []
y.append([524.61, 835.26, 826.14, 1028.42, 1291.29, 524.61, 835.26, 826.14, 1028.42, 1291.29, 1042.12, 819.56, 1042.12, 819.56])
y.append([621, 987, 939, 1211, 1783, 625, 987, 934, 1211, 1783, 1209, 893, 1209, 870])
y.append([618, 900, 869, 1176, 1463, 618, 900, 869, 1176, 1463, 1081, 824, 1081, 824])
y.append([558, 911, 864, 1186, 1464, 558, 911, 864, 1186, 1464, 1077, 834, 1077, 834])
y.append([614, 909, 898, 1123, 1437, 614, 909, 898, 1123, 1437, 1156, 826, 1156, 826])
y.append([620, 939, 926, 1114, 1441, 620, 939, 926, 1114, 1441, 1179, 879, 1179, 879])
y = np.array(y)
labels = ["最优解", "or_tool", "最佳_最远", "第一_最远", "最佳_最近", "第一_最近"]

for i in range(y.shape[0]):
    #plt.scatter(x=x, y=y[i], c='b', s=1)
    #plt.plot(x, y[i], label=labels[i], linewidth=1)
    plt.plot(x, y[i], linewidth=1)
    #plt.legend()

plt.xticks(c='w')
plt.yticks(c='w')
plt.savefig("1.jpg")
plt.cla()

# time
t = []
t.append([5.03, 10.05, 8.04, 12.07, 16.1, 5.02, 10.05, 8.04, 12.08, 16.1, 7.03, 10.04, 7.04, 10.04])
t.append([1, 1.24, 1.44, 1.78, 3.9, 0.77, 0.96, 1.31, 1.59, 3.92, 0.78, 1.05, 0.75, 1.06])
t = np.array(t)
labels = ["or_tool", "第一_最远"]

for i in range(t.shape[0]):
    # plt.scatter(x=x, y=t[i], c='b', s=1)
    # plt.plot(x, t[i], label=labels[i], linewidth=1)
    plt.plot(x, t[i], linewidth=1)
    # plt.legend()

plt.xticks(c='w')
plt.yticks(c='w')
plt.savefig("2.jpg")
plt.cla()

# single
z = []
z.append([558, 911, 864, 1186, 1464, 558, 911, 864, 1186, 1464, 1077, 834, 1077, 834])
z.append([772, 1053, 1140, 1357, 1663, 772, 1053, 1140, 1357, 1663, 1256, 1011, 1256, 1011])
z.append([589, 938, 921, 1267, 1524, 589, 938, 921, 1267, 1524, 1242, 939, 1242, 939])
z.append([695, 966, 1022, 1226, 1554, 695, 966, 1022, 1226, 1554, 1095, 889, 1095, 889])
z = np.array(z)
labels = ["第一_最远", "仅初始化", "仅路径间搜索", "仅路径内搜索"]

for i in range(z.shape[0]):
    # plt.scatter(x=x, y=z[i], c='b', s=1)
    # plt.plot(x, z[i], label=labels[i], linewidth=1)
    plt.plot(x, z[i], linewidth=1)
    # plt.legend()

plt.xticks(c='w')
plt.yticks(c='w')
plt.savefig("3.jpg")
plt.cla()




