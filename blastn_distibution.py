import pandas as pd
import matplotlib.pyplot as plt

def load_data_and_plot(file_path_gRNA, file_path_WT, title):
    data1 = pd.read_table(file_path_gRNA, sep='\t')
    data2 = pd.read_table(file_path_WT, sep='\t')

    fig, ax = plt.subplots()
    bar_width = 0.35

    # 对data1的sseqid进行计数并降序排序
    chromosome_counts1 = data1['sseqid'].value_counts().sort_values(ascending=False)
    chromosome_counts2 = data2['sseqid'].value_counts().reindex(chromosome_counts1.index, fill_value=0)

    index = range(len(chromosome_counts1))

    for i, (chromosome_counts, color, label) in enumerate(zip([chromosome_counts1, chromosome_counts2], ['r', 'b'], ['gRNA', 'WT'])):
        positions = [x + bar_width * i for x in index]
        ax.bar(positions, chromosome_counts, width=bar_width, color=color, alpha=0.5, label=label)

    ax.set_xlabel('Chromosome')
    ax.set_ylabel('Number of Rows')
    ax.set_xticks([x + bar_width / 2 for x in index])
    ax.set_xticklabels(chromosome_counts1.index, rotation=45)
    ax.xaxis.set_tick_params(labelsize=6)
    ax.legend(loc='upper right')
    ax.set_title(title)
    plt.show()

# 加载并绘制conf_insert数据
load_data_and_plot('test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz.conf_insert.tbl.gz',
                   'test/WT_S15_L001_index_unmappedphix_merged.assembled.fasta.gz.conf_insert.tbl.gz',
                   'conf_insert')

# 加载并绘制conf_non_insert数据
load_data_and_plot('test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz.conf_non_insert.tbl.gz',
                   'test/WT_S15_L001_index_unmappedphix_merged.assembled.fasta.gz.conf_non_insert.tbl.gz',
                   'conf_non_insert')

# 加载并绘制potential_insert数据
load_data_and_plot('test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz.potential_insert.tbl.gz',
                   'test/WT_S15_L001_index_unmappedphix_merged.assembled.fasta.gz.potential_insert.tbl.gz',
                   'potential_insert')

