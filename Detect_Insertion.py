import pandas as pd
import argparse
import gzip
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser(description="Detect and classify insertion from blastn results")
    parser.add_argument('-i', '--input', required=True, help='Input blastn results tbl file.')
    parser.add_argument('-fa', '--fasta', required=True, help='Assembled fasta file.')
    parser.add_argument('-rc', '--reference_chr', required=True, help='The chromosome of reference region.')
    parser.add_argument('-rs', '--reference_start', required=True, help='Reference start position')
    parser.add_argument('-re', '--reference_end', required=True, help='Reference end position')
    parser.add_argument('--insert_size', required=True, help='The minimal size of insertion')
    parser.add_argument('--reference_size', required=True, help='The size of reference region.')
    return parser.parse_args()

def filter_blastn_results(blastn_df, rchr, rstart, rend, length, minregionsize):
    # 定义筛选条件
    conf_non_insert = (blastn_df['sseqid'] == rchr) & (blastn_df['sstart'].between(rstart, rend)) & (blastn_df['send'].between(rstart, rend)) & (blastn_df['length'] >= length) & (blastn_df['qlen'] <= minregionsize)
    
    # 使用 conf_non_insert 条件筛选数据
    non_insert_df = blastn_df[conf_non_insert]
    
    # 从原始 DataFrame 中去除已筛选的数据
    remaining_df = blastn_df[~conf_non_insert]
    
    # 定义其他筛选条件
    conf_insert = (remaining_df['sseqid'] != rchr) | ~remaining_df['sstart'].between(rstart, rend)
    insert_df = remaining_df[conf_insert]

    remaining_df = remaining_df[~conf_insert]

    potential_insert = remaining_df['qlen'] > minregionsize
    
    # 应用剩余的筛选条件
    potential_insert_df = remaining_df[potential_insert]
    
    # 将结果存储在字典中
    results = {
        'conf_non_insert': non_insert_df,
        'conf_insert': insert_df,
        'potential_insert': potential_insert_df
    }
    
    return results

def write_results_to_files(fa, results):
    for key, df in results.items():
        with gzip.open(f"{fa}.{key}.tbl.gz", 'wt') as file:
            file.write(df.to_csv(sep='\t', index=False))

def process_blastn_res(path, rstart, rend, rchr, minregionsize, fa, length=80):
    blastnres_header = "qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen bitscore evalue"
    blastnres = pd.read_table(path, sep='\t', header=None, names=blastnres_header.split())
    results = filter_blastn_results(blastnres, rchr, rstart, rend, length, minregionsize)
    write_results_to_files(fa, results)
    return results

def extract_fasta(fa, results):
    with gzip.open(fa, 'rt') as handle:
        # 将所有FASTA序列读入字典，键为序列ID
        fasta_dict = {fasta.id: fasta for fasta in SeqIO.parse(handle, 'fasta')}
        
    for key, df in results.items():
        # 根据df中的qseqid筛选需要的FASTA序列
        selected_fastas = (fasta_dict[seqid] for seqid in df['qseqid'] if seqid in fasta_dict)
        
        # 创建一个集合来存储已经写入的序列ID，以避免重复写入
        written_ids = set()
        
        with gzip.open(f"{fa}.{key}.fa.gz", 'wt') as file:
            # 过滤掉已经写入的序列
            unique_fastas = (fasta for fasta in selected_fastas if fasta.id not in written_ids and not (written_ids.add(fasta.id)))
            SeqIO.write(unique_fastas, file, 'fasta')

def main():
    args = parse_args()
    results = process_blastn_res(path=args.input, rstart=int(args.reference_start), rend=int(args.reference_end), 
                                 rchr=args.reference_chr, minregionsize=int(args.insert_size) + int(args.reference_size), 
                                 fa=args.fasta)
    extract_fasta(args.fasta, results)

if __name__ == "__main__":
    main()

# python Detect_Insertion.py -i test/WT_S15_L001_index_unmappedphix_merged.assembled.fasta.gz.tbl.gz -fa test/WT_S15_L001_index_unmappedphix_merged.assembled.fasta.gz -rc chrX -rs 134498370 -re 134498450 --insert_size 10 --reference_size 85 & python Detect_Insertion.py -i test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz.tbl.gz -fa test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz -rc chrX -rs 134498371 -re 134498450 --insert_size 10 --reference_size 85 &
