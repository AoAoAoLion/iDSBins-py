#!/usr/bin/python3

import Bio.SeqIO as SeqIO
from collections import Counter
import random
import argparse
import gzip

def extract_index(fastq_file):
    # 根据文件扩展名确定打开方式
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
    parser = argparse.ArgumentParser(description="提取并显示一个或多个FASTQ文件中最常见序列的前三个字母")
    parser.add_argument("fastq_files", type=str, nargs='+', help="一个或多个FASTQ文件的路径")
    args = parser.parse_args()

    for fastq_file in args.fastq_files:
        index = extract_index(fastq_file)
        print(f"在 {fastq_file} 中最常见的序列的前三个字母是: {index}")

if __name__ == "__main__":
    main()

