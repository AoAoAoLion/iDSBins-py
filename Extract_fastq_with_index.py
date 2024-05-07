#!/usr/bin/python3

import Bio.SeqIO as SeqIO
from collections import Counter
import random
import argparse
import gzip
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Process FASTQ files.')
    parser.add_argument('-f', '--ffastq', required=True, help='Forward reads (FASTQ format)')
    parser.add_argument('-r', '--Rfastq', required=True, help='Reverse reads (FASTQ format)')
    parser.add_argument('-i', '--forward_index', help='Forward index')
    parser.add_argument('-g', '--reverse_index', help='Reverse index')
    parser.add_argument('-o', '--output_dir', required=True, help='Output directory')
    return parser.parse_args()

def open_fastq(file_path):
    if file_path.endswith('.gz'):
        return gzip.open(file_path, 'rt')  # 'rt' mode for reading text from a gzipped file
    else:
        return open(file_path, 'r')

def open_output_fastq(output_dir, base_name, suffix):
    output_path = os.path.join(output_dir, f"{base_name}{suffix}.fastq.gz")
    return gzip.open(output_path, 'wt')  # 'wt' mode for writing text to a gzipped file

def extract_index(fastq_file):
    # 根据文件扩展名��定打开方式
    open_func = gzip.open if fastq_file.endswith('.gz') else open
    # 打开并读取FASTQ文件
    with open_func(fastq_file, "rt") as fq:  # 使用"rt"模式以文本方式读取
        # 读取所有序列记录
        all_records = list(SeqIO.parse(fq, "fastq"))
        # 随机选择1000个序列记录
        selected_records = random.sample(all_records, 1000)

    # 提取每个记录的序列
    sequences = [str(record.seq) for record in selected_records]

    # 使用Counter来找出最常见的序列
    most_common_sequence = Counter(sequences).most_common(1)[0][0]
    # 获取最常见序列的前三个字母
    first_three_letters = most_common_sequence[:3]
    return first_three_letters 

def main():
    args = parse_args()

    # 如果没有提供索引，则自动从第一个文件中提取
    if args.forward_index is None or args.reverse_index is None:
        if args.ffastq:
            args.forward_index = extract_index(args.ffastq)
            print(f"自动选择的前向索引: {args.forward_index}")
        if args.Rfastq:
            args.reverse_index = extract_index(args.Rfastq)
            print(f"自动选择的反向索引: {args.reverse_index}")

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Extract base names without extensions
    base_name_f = os.path.splitext(os.path.splitext(os.path.basename(args.ffastq))[0])[0]
    base_name_r = os.path.splitext(os.path.splitext(os.path.basename(args.Rfastq))[0])[0]

    # Open input FASTQ files with potential gzip handling
    forward_reads = SeqIO.parse(open_fastq(args.ffastq), "fastq")
    reverse_reads = SeqIO.parse(open_fastq(args.Rfastq), "fastq")

    # Open output files with gzip compression and modified names
    with open_output_fastq(args.output_dir, base_name_f, '_index') as pair1, \
         open_output_fastq(args.output_dir, base_name_r, '_index') as pair2, \
         open_output_fastq(args.output_dir, base_name_f, '_unindex') as upair1, \
         open_output_fastq(args.output_dir, base_name_r, '_unindex') as upair2:

        # Process each pair of reads
        for read1, read2 in zip(forward_reads, reverse_reads):
            if read1.seq.startswith(args.forward_index) and read2.seq.startswith(args.reverse_index):
                SeqIO.write(read1, pair1, "fastq")
                SeqIO.write(read2, pair2, "fastq")
            else:
                SeqIO.write(read1, upair1, "fastq")
                SeqIO.write(read2, upair2, "fastq")

if __name__ == "__main__":
    main()
