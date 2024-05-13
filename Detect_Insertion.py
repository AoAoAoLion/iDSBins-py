import pandas as pd
import argparse

def parse_args():
    # construct arguments
    parser = argparse.ArgumentParser(description="Detect and classify insertion from blastn results")
    parser.add_argument('-i', '--input', required=True, help='Input blastn results tbl file.')
    parser.add_argument('-o', '--output', required=True, help='Output suffix.')
    parser.add_argument('-fa', '--fasta', required=True, help='Assembled fasta file.')
    parser.add_argument('-rc', '--reference_chr', required=True, help='The chromosome of reference region.')
    parser.add_argument('-s', '--start', required=True, help='Reference start position')
    parser.add_argument('-e', '--end', required=True, help='Reference end position')
    parser.add_argument('--insert', required=True, help='The minimal size of insertion')
    parser.add_argument('--size', required=True, help='The size of reference region.')
    return parser.parse_args()


# Load Blastn results

blastn_res = pd.read_table()