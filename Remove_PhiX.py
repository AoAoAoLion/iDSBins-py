import os
import argparse

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="Run bbduk.sh with specified parameters.")
parser.add_argument("sample_id", required=True, help="Sample ID to process")
parser.add_argument("--bbmappath", required=True, help="Base path to the BBMap software")
args = parser.parse_args()

bbmappath = args.bbmappath
SampleID = args.sample_id

command = f"{bbmappath}/bbmap/bbduk.sh -in1={SampleID}_filter.R1.fastq in2={SampleID}_filter.R2.fastq " \
          f"out1={SampleID}_filter.unmaped.R1.fastq out2={SampleID}_filter.unmaped.R2.fastq " \
          f"outm1={SampleID}_filter.mappedphix.R1.fastq outm2={SampleID}_filter.mappedphix.R2.fastq " \
          f"ref={bbmappath}/bbmap/resources/phix_adapters.fa.gz k=31 hdist=2 stats=stats.txt"

os.system(command)

