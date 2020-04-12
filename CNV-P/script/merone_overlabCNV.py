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
	'-b',
	'--bed',
	type=str,
	default=None,
	metavar='bed',
	help='Sorted cnv file'
)


args = ap.parse_args()

######################

def Get_one_overCNV(file1):
	Chr={}
	pos_r=0
	pos_l=0
	for line in file1:
		line=line.strip("\n")
		line_list=line.split("\t")
		chrom=line_list[0]
		if line_list[4]=="INS":
			print(line)
			continue
		pos_l=int(line_list[1])
		pos_r=int(line_list[2])
		#if pos_r - pos_l == 0: print(line_list)
		if chrom not in Chr.keys():
			Chr[chrom]=line_list
			#print(chrom)
		else:
			pos_l0=int(Chr[chrom][1])
			pos_r0=int(Chr[chrom][2])
			type_cnv=Chr[chrom][4]
			out = "\t".join(map(str,(Chr[chrom])))
			if pos_l > pos_r0 or pos_r < pos_l0:
				print("{}".format(out))
				Chr[chrom]=line_list
			else:
				overlab=min(abs(pos_l-pos_r0),abs(pos_l0-pos_r))
				length=min(pos_r-pos_l,pos_r0-pos_l0)
				if overlab/length>=0.8:
					if type_cnv != line_list[4]:continue
					arr=sorted([pos_l,pos_r,pos_l0,pos_r0])
					Chr[chrom][1]=arr[0]
					Chr[chrom][2]=arr[-1]
					Chr[chrom][3]=arr[-1]-arr[0]+1
				else:
					print("{}".format(out))
					Chr[chrom]=line_list

	file1.close()


if __name__ == "__main__":
	f=open(args.bed,"r")
	Get_one_overCNV(f)
