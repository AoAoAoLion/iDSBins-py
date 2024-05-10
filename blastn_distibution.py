import pandas as pd
import matplotlib.pyplot as plt

# 加载数据
data1 = pd.read_table('/rsrch4/home/ccp-rsch/swu12/Project#DSBs_Insertion/iDSBins-py/test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz.tbl.gz', sep= '\t', header=None)
data2 = pd.read_table('test/WT_S15_L001_index_unmappedphix_merged.assembled.fasta.gz.tbl.gz', sep= '\t', header=None)

# 过滤掉特定的数据行
data1 = data1[~((data1[1] == 'chrX') & (data1[9] == 134498371) & (data1[10] == 134498450))]
data2 = data2[~((data2[1] == 'chrX') & (data2[9] == 134498371) & (data2[10] == 134498450))]

# 设置图形
fig, ax = plt.subplots()

# 定义条形图的宽度和位置调整
bar_width = 0.35
index = range(len(data1[1].unique()))

# 绘制每个染色体的匹配查询分布
for i, (data, color, label) in enumerate(zip([data1, data2], ['r', 'b'], ['gRNA', 'WT'])):
    # 计算每个染色体的行数
    chromosome_counts = data[1].value_counts().sort_index()
    # 为每个数据集调整位置
    positions = [x + bar_width * i for x in index]
    
    ax.bar(positions, chromosome_counts.reindex(data1[1].unique(), fill_value=0), width=bar_width, color=color, alpha=0.5, label=label)

# 添加染色体标签并设置字体大小
ax.set_xlabel('Chromosome', fontsize=7)  
ax.set_ylabel('Number of Rows')

# 设置x轴刻度标签并旋转标签角度
ax.set_xticks([x + bar_width / 2 for x in index])
ax.set_xticklabels(data1[1].unique(), rotation=45)

# 设置图形属性
ax.legend(loc='upper right')

# 显示图形
plt.show()
