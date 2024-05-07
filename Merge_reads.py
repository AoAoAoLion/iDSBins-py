import os
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run PEAR with specified parameters.")
    parser.add_argument("--sample_id", required = True, help="Sample ID to process")
    return parser.parse_args()

def construct_command(args):
    sample_id = args.sample_id
    return (f"pear -f {sample_id}_R1_001_index_unmapedphix.fastq.gz -r {sample_id}_R2_001_index_unmapedphix.fastq.gz "
            f"-o {sample_id}_index_mappedphix_merged -j 4")

def gzip_command(args):
    sample_id = args.sample_id
    return (f"gzip {sample_id}*fastq")

def run_command(command):
    os.system(command)

def main():
    args = parse_arguments()
    command = construct_command(args)
    run_command(command)
    gzip = gzip_command(args)
    run_command(gzip)

if __name__ == "__main__":
    main()
