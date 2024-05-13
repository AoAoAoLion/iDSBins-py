import pandas as pd
import argparse

def parse_args():
    # construct arguments
    parser = argparse.ArgumentParser(description="Detect and classify insertion from blastn results")
    parser.add_argument('-i', '--input', required=True, help='Input blastn results tbl file.')
    parser.add_argument('-o', '--output', required=True, help='Output suffix.')
    parser.add_argument('-fa', '--fasta', required=True, help='Assembled fasta file.')
    parser.add_argument('-rc', '--reference_chr', required=True, help='The chromosome of reference region.')
    parser.add_argument('-rs', '--reference_start', required=True, help='Reference start position')
    parser.add_argument('-re', '--reference_end', required=True, help='Reference end position')
    parser.add_argument('--insert_size', required=True, help='The minimal size of insertion')
    parser.add_argument('--reference_size', required=True, help='The size of reference region.')
    return parser.parse_args()

def process_blastn_res(path, rstart, rend, rchr, minregionsize, length = 80):
    conf_non_insert = None
    conf_insert = None
    potential_insert = None
    rstart = int(rstart)
    rend=int(rend)
    minregionsize=int(minregionsize)
    length = int(length)
    blastnres_header = "qseqid sseqid pident length mismatch gapopen qstart qend qlen sstart send slen bitscore evalue"
    blastnres = pd.read_table(path, sep= '\t', header=None, names=blastnres_header.split())
    conf_non_insert = blastnres[~(blastnres['sseqid'] == rchr) & 
                                (blastnres['qstart'] >= rstart) & (blastnres['qstart'] <= rend) & (blastnres['qend'] >= rstart) & (blastnres['qend'] >= rend) &
                                (blastnres['length'] >= length) & (blastnres['qlen'] <= minregionsize)]
    conf_insert = blastnres[~(blastnres['sseqid'] != rchr) | (blastnres['qstart'] < rstart) | (blastnres['qstart'] > rend)]
    potential_insert = blastnres[~(blastnres['qlen'] > minregionsize)]

    return (conf_non_insert, conf_insert, potential_insert)

def main():
    args = parse_args()
    blastnres = process_blastn_res(path = args.input, rstart = int(args.reference_start), rend = int(args.reference_end), rchr = args.reference_chr,
                                   minregionsize = int(args.insert_size) + int(args.reference_size))
    for i in [0,1,2]:
        print(i)
        print(blastnres[i])



if __name__ == "__main__":
    main()




#python Detect_Insertion.py -i test/gRNA-Puroblast_S12_L001_index_unmappedphix_merged.assembled.fasta.gz.tbl.gz -o oo -fa ff -rc chrX -rs 134498371 -re 134498450 --insert_size 10 --reference_size 85