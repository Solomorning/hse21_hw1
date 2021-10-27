# hse21_hw1
ls -1 /usr/share/data-minor-bioinf/assembly/* | xargs -tI{} ln -s {}
seqtk sample -s713 oil_R1.fastq 5000000 > paired_end_1.fastq
seqtk sample -s713 oil_R2.fastq 5000000 > paired_end_2.fastq
seqtk sample -s713 oilMP_S4_L001_R1_001.fastq 1500000 > MP_r1_001.fastq
seqtk sample -s713 oilMP_S4_L001_R2_001.fastq 1500000 > MP_r2_001.fastq
mkdir fastqc
ls *.fastq | xargs -P 4 -tI{} fastqc -o fastqc {}
mkdir multiqc
multiqc -o multiqc fastqc
platanus_trim paired_end_1.fastq paired_end_2.fastq
platanus_internal_trim MP_r1_001.fastq MP_r2_001.fastq
mkdir trimmed_fastqc
ls *.trimmed| xargs -P 4 -tI{} fastqc -o trimmed_fastqc {}
mkdir trimmed_multiqc
multiqc -o trimmed_multiqc trimmed_fastqc
platanus assemble -o Poil -t 8 -m 28 -f paired*.trimmed paired*.trimmed 2> assemble.log
platanus scaffold -o Poil -t 8 -c Poil_contig.fa -IP1 paired*.trimmed -OP2 MP*.trimmed 2> scaffold.log
platanus gap_close -o Poil -t 8 -c  Poil_scaffold.fa -IP1 paired*.trimmed -OP2 MP*.trimmed 2> gapclose.log
echo scaffol_cov231 > _tmp.txt
seqtk subseq Poil_gapclosed.fa _tmp.txt > oil_genome.fna
