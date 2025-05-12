import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import ScalarFormatter

# 文件路径（字符串表示）
file_path = ""

# 读取CSV文件
df = pd.read_csv(file_path, sep=',')  

# 计算每种算法在不同线程数下的平均时间
avg_times = df.groupby(['algo_name', 'cache_mb'])['time'].mean().unstack(level=0)

# 绘制折线图
plt.figure(figsize=(6, 4))
for algo in avg_times.columns:
    plt.plot(avg_times.index, avg_times[algo], marker='o', label=algo)

plt.xlabel('CacheSize (MB)')
plt.ylabel('Running Time (ms)')
plt.title('Performance of BFS Algorithms (Dataset: APN)')

# 设置纵坐标为科学计数法（10的几次方）
plt.yscale('log')  # 使用对数坐标
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))  # 科学计数法显示
plt.gca().yaxis.get_major_formatter().set_scientific(True)
plt.gca().yaxis.get_major_formatter().set_powerlimits((0, 0))  # 强制显示指数



plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xscale('log', base=2)  # 横坐标对数刻度（2的幂）
plt.xticks(avg_times.index, avg_times.index)  # 显示所有线程数
plt.tight_layout()
plt.show()