import Read_File as rf
import Get_Feature as gf
import pysam as ps
import numpy as np
import sys


#Defind the USAGE
import argparse

class CapitalisedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
	def add_usage(self, usage, actions, groups, prefix=None):
		if prefix is None:
			prefix = 'Usage: '
			return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

ap = argparse.ArgumentParser(formatter_class=CapitalisedHelpFormatter)


ap.add_argument(
	'-bed',
	'--bedfile',
	type=str,
	default=None,
	metavar='CNV_bed',
	required=True,
	help='path to a .bed file with locations of CNVs. The second column should be CNV start, and the third column should be CNV end '
)

ap.add_argument(
	'-bam',
	'--bamfile',
	type=str,
	default=None,
	required=True,
	metavar='bamfile',
	help='input bam file'
)

ap.add_argument(
	'-bas',
	'--bas_file',
	type=str,
	default=None,
	metavar='bas_file',
	help='path to a .bas file'
)

ap.add_argument(
	'-s',
	'--sample',
	type=str,
	default=None,
	metavar='samplename',
	help='names of sample'
)

ap.add_argument(
	'-o',
	'--output',
	type=str,
	default='.',
	metavar='outdir',
	help='the directory into which output files will go'
)

args = ap.parse_args()





def Make_result(CNV_bed,sam_file,RG_bas_dict,outdir,sample):
	f = open(outdir+".feature.txt",'w')

	bed_len = len(CNV_bed)
	print("bed_len %d"%bed_len)
	for i in range(bed_len):
		print("i = %d"%i)
		depth,gc_cont=gf.Get_Depth(sam_file,CNV_bed[i][0],int(CNV_bed[i][1]),int(CNV_bed[i][2]),RG_bas_dict,sample)
		sr_l,pem_l=gf.Get_Feature(sam_file,CNV_bed[i][0],int(CNV_bed[i][1])-500,int(CNV_bed[i][1])+500,RG_bas_dict,sample)
		sr_r,pem_r=gf.Get_Feature(sam_file,CNV_bed[i][0],int(CNV_bed[i][2])-500,int(CNV_bed[i][2])+500,RG_bas_dict,sample)
		out="\t".join(CNV_bed[i])
		chrr=CNV_bed[i][0].replace('chr','')
		fea="\t".join(map(str,[depth,gc_cont,sr_l,pem_l,sr_r,pem_r,chrr]))
		f.write(out+"\t"+fea+"\n")




if __name__ == "__main__":
        #reading file
	CNV_bed=rf.Read_bed(args.bedfile)
	bamfile=rf.Read_bam(args.bamfile)
	RG_bas=rf.Read_bas(args.bas_file)
	outdir=args.output
	sample=args.sample
	#print
	Make_result(CNV_bed,bamfile,RG_bas,outdir,sample)
