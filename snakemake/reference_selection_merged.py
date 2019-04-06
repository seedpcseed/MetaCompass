"""
DESCRIPTION
"""
#__author__ = "Victoria Cepeda

#configfile: expand("config.json",

#include_prefix="https://"
#include_prefix + "rules"

#os.system("touch %s"%config['reads'][0])


#ruleorder: merge_reads > kmer_mask > fastq2fasta > reference_recruitment > mash_filter > bowtie2_map > build_contigs > pilon_map > sam_to_bam > bam_sort > pilon_contigs > remove_zerocov >  assemble_unmapped > join_contigs

ruleorder: merge_reads > kmer_mask > fastq2fasta > reference_recruitment 

#ruleorder: bowtie2_map > assemble_unmapped > build_contigs > pilon_map > sam_to_bam > bam_sort > pilon_contigs
#code to skip initial steps if reference genomes provided 
if config['reads'] != "" and config['reference'] != "%s"%expand('{prefix}/{sample}.0.assembly.out/mc.refseq.fna',sample=config['sample'],prefix=config["prefix"])[0]:
     os.system("touch %s"%expand('{prefix}/{sample}.marker.match.1.fastq',prefix=config['prefix'],sample=config['sample'])[0])
     os.system("touch %s"%expand('{prefix}/{sample}.fasta',prefix=config['prefix'],sample=config['sample'])[0])
     os.system("mkdir -p %s"%expand('{prefix}/{sample}.0.assembly.out',prefix=config['prefix'],sample=config['sample'])[0])
     os.system("mkdir -p %s"%expand('{prefix}/{sample}.{iter}.assembly.out',prefix=config['prefix'],sample=config['sample'],iter=config['iter'])[0])
rule all:
    input:expand('{prefix}/{sample}.0.assembly.out/mc.refseq.fna',prefix=config['prefix'],sample=config['sample'])
#out=expand('{prefix}/{sample}.{iter}.assembly.out',prefix=config['prefix'],sample=config['sample'],iter=config['iter']),reffile =expand('{prefix}/{sample}.0.assembly.out/mc.refseq.fna',prefix=config['prefix'],sample=config['sample']),refids=expand('{prefix}/{sample}.0.assembly.out/mc.refseq.ids',prefix=config['prefix'],sample=config['sample'])

rule merge_reads:
    input:
        reads=config['reads'].split(",")[0]
    message: """---merge fastq reads"""
    output:
        merged='%s/%s.merged.fq'%(config['prefix'],config['sample'])
    run:

        for read in config['reads'].split(','):
            if read != "" and len(read) != 0:
                os.system("cat %s >> %s/%s.merged.fq"%(read,config['prefix'],config['sample']))
        if config['reads'] != "" and config['reference'] != "%s"%expand('{prefix}/{sample}.0.assembly.out/mc.refseq.fna',sample=config['sample'],prefix=config["prefix"])[0]:
             os.system("touch %s"%expand('{prefix}/{sample}.marker.match.1.fastq',prefix=config['prefix'],sample=config['sample'])[0])
             os.system("touch %s"%expand('{prefix}/{sample}.fasta',prefix=config['prefix'],sample=config['sample'])[0])
             os.system("mkdir -p %s"%expand('{prefix}/{sample}.0.assembly.out',prefix=config['prefix'],sample=config['sample'])[0])
             os.system("mkdir -p %s"%expand('{prefix}/{sample}.{iter}.assembly.out',prefix=config['prefix'],sample=config['sample'],iter=config['iter'])[0])
             os.system("touch %s"%expand('{prefix}/{sample}.0.assembly.out/mc.refseq.fna',prefix=config['prefix'],sample=config['sample'])[0])


rule kmer_mask:
    input:
        r1=rules.merge_reads.output.merged
    output:
        fastq1=expand('{prefix}/{sample}.marker.match.1.fastq',prefix=config['prefix'],sample=config['sample'])[0],
    message: """---kmer-mask fastq"""
    params:
        out=expand('{prefix}/{sample}.marker',prefix=config['prefix'],sample=config['sample'])[0],
        len=str(int(config["length"])+3)
    threads:int(config['nthreads'])
    log:'%s/%s.%s.kmermask.log'%(config['prefix'],config['sample'],config['iter'])
    shell:"echo kmer-mask -ms 28 -mdb %s/refseq/kmer-mask_db/markers.mdb -1 {input.r1} -clean 0.0 -match 0.01 -nomasking -t {threads} -l {params.len} -o {params.out} ; kmer-mask -ms 28 -mdb %s/refseq/kmer-mask_db/markers.mdb -1 {input.r1} -clean 0.0 -match 0.01 -nomasking -t {threads} -l {params.len} -o {params.out} 1>> {log} 2>&1"%(config["mcdir"],config["mcdir"])


rule fastq2fasta:
    input: rules.kmer_mask.output.fastq1
    output:expand('{prefix}/{sample}.fasta',prefix=config['prefix'],sample=config['sample'])
    message: """---Converting fastq to fasta."""
    shell : "perl %s/bin/fq2fa.pl -i {input} -o {output}"%(config["mcdir"])
    log:'%s/%s.%s.fastq2fasta.log'%(config['prefix'],config['sample'],config['iter'])

#    benchmark:
#       "%s/benchmarks/reference_recruitment/%s.txt"%(config['prefix'],config['sample'])

#fqfile =expand('{prefix}/{sample}.0.assembly.out/{sample}.fq',prefix=config['prefix'],sample=config['sample'])
#'{prefix}/{sample}.{iter}.assembly.out/mc.refseq.fna'
rule reference_recruitment:
    input:
        fasta = rules.fastq2fasta.output,
        fastq = rules.merge_reads.output
    params:
        cogcov = "%d"%(int(config['cogcov'])),
        readlen = "%d"%(int(config['length']))
    output:
        out =expand('{prefix}/{sample}.{iter}.assembly.out',prefix=config['prefix'],sample=config['sample'],iter=config['iter']),
	    reffile =expand('{prefix}/{sample}.0.assembly.out/mc.refseq.fna',prefix=config['prefix'],sample=config['sample']),
        refids=expand('{prefix}/{sample}.0.assembly.out/mc.refseq.ids',prefix=config['prefix'],sample=config['sample'])
    message: """---reference recruitment."""
    threads:int(config['nthreads'])
    log:'%s/%s.%s.reference_recruitement.log'%(config['prefix'],config['sample'],config['iter'])
    shell:"mkdir -p {output.out}; python3 %s/bin/select_references.py {input.fasta} {input.fastq} {output.out} {threads} {params.cogcov}  1>> {log} 2>&1"%(config["mcdir"])

#rule mash_filter:
#    input:
#        r1=rules.merge_reads.output.merged,
#        g1=rules.reference_recruitment.output.reffile
#    output:
#        reffile=expand('{prefix}/{sample}.0.assembly.out/mc.refseq.filt.fna',prefix=config['prefix'],sample=config['sample'])
#    params:
#        mfilter= "%f"%(float(config['mfilter']))
#    message: """---mash filter recruited references"""
#    threads:int(config["nthreads"])
#    log:'%s/%s.%s.mash.log'%(config['prefix'],config['sample'],config['iter'])
#    shell:"echo {params.mfilter};python3 %s/bin/mash_filter.py {input.r1} {input.g1} {output.reffile} {params.mfilter} 1>> {log} 2>&1"%(config["mcdir"])

