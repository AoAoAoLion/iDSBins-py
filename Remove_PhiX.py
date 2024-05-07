import os
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run bbduk.sh with specified parameters.")
    parser.add_argument("--sample_id", help="Sample ID to process")
    parser.add_argument("--phix", required=True, help="Base path to the PhiX reference")
    return parser.parse_args()

def construct_command(args):
    phix = args.phix
    sample_id = args.sample_id
    return (f"bbduk.sh -in1={sample_id}_R1_001_index.fastq.gz in2={sample_id}_R2_001_index.fastq.gz "
            f"out1={sample_id}_R1_001_index_unmapedphix.fastq.gz out2={sample_id}_R2_001_index_unmapedphix.fastq.gz "
            f"outm1={sample_id}_R1_001_index_mappedphix.fastq.gz outm2={sample_id}_R2_001_index_mappedphix.fastq.gz "
            f"ref={phix} k=31 hdist=2 stats={sample_id}_stats.txt overwrite=t")

def run_command(command):
    os.system(command)

def main():
    args = parse_arguments()
    command = construct_command(args)
    run_command(command)

if __name__ == "__main__":
    main()
