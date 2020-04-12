import pysam as ps
import os


def Read_bed(bed):
	if not os.path.isfile(bed):
		print('Bedfile does not exist at location provided, please check (tried "{}")'.format(bed))
		exit(2)
	print("Loading bed file: {} ...".format(bed))
	bed_f = open(bed)
	CNV_bed=[]
	for line in bed_f:
		line=line.strip("\n")
		line_list=line.split("\t")
		CNV_bed.append(line_list)
	bed_f.close()
	return CNV_bed

def Read_bas(bas):
	if not os.path.isfile(bas):
		print('Bedfile does not exist at location provided, please check (tried "{}")'.format(bas))
		exit(2)
	print("Loading bas file: {} ...".format(bas))
	bas_f = open(bas)
	RG_bas={}
	for line in bas_f:
		line=line.strip("\n")
		line_list=line.split("\t")
		RG_bas[line_list[6]]=line_list[17]+"\t"+line_list[18]+"\t"+line_list[-1]
	bas_f.close()
	return RG_bas

def Read_bam(bam):
	print("Loading bam file: {} ...".format(bam))
	bamfile = ps.AlignmentFile(bam, 'rb')
	try:
		bamfile.check_index()
		print('Index file found - {}'.format(bam + '.bai'))
	except ValueError:
		print('Index file not found (should be named "{}.bai" and located in the same directory)'.format(bam))
	return bamfile
