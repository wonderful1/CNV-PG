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
	'-N',
	'--N_region',
	type=str,
	default="/home/sunjinghua/database/my_database_dir/artificial_region/N.region_hg19",
	metavar='N_regionFile',
	help='a bed file specifies the N region in genome'
)

ap.add_argument(
	'-C',
	'--CNV_bedfile',
	type=str,
	default=None,
	metavar='CNV_bedfile',
	help='path to CNV file'
)


args = ap.parse_args()

############################


def Remove_NRe_SuperDups_MapEx(file1,file2):
	chr={}
	for line1 in file1:
		line1=line1.strip("\n")#只能删除开头和结尾的字符
		line1_list=line1.split("\t")
		if line1_list[0]== 'Chr':continue
		if line1_list[0] not in chr.keys():
			chr[line1_list[0]]=line1_list[1]+"\t"+line1_list[2]
		else:
			chr[line1_list[0]]=chr[line1_list[0]]+"\n"+line1_list[1]+"\t"+line1_list[2]
		
	for line2 in file2:
		line2=line2.strip("\n")#只能删除开头和结尾的字符
		line2_list=line2.split("\t")
		if line2_list[0] == 'chrY'or line2_list[0] == 'chrM' or len(line2_list[0]) > 5 : continue
		if int(line2_list[1]) > int(line2_list[2]):continue
		if line2_list[0] not in chr.keys(): 
			print(line2)
			continue
		file1_list=chr[line2_list[0]].split("\n")
		overlab='NA'
		for cnv in file1_list:
			cnv_list=cnv.split("\t")
			if cnv == "" :continue
			else:
				pos_l=int(line2_list[1] )
				pos_r=int(line2_list[2])
				pos_l0=int(cnv_list[0])
				pos_r0=int(cnv_list[1])
				
				if pos_l >= pos_r0 or pos_r <= pos_l0:
					overlab=0
				else:
					overlab=1
					break
		if overlab ==0 :
			print(line2)			
		else:continue
	
				
if __name__ == "__main__":
	f1=open(args.N_region,"r")
	f2=open(args.CNV_bedfile,"r")
	Remove_NRe_SuperDups_MapEx(f1,f2)

