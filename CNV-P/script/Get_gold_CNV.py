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
	'-g',
	'--goldCNV',
	type=str,
	default=None,
	required=True,
	metavar='goldCNVfile',
	help='a file provide gold-stadard CNV' 
)

ap.add_argument(
	'-f',
	'--inputfile',
	type=str,
	default=None,
	required=True,
	metavar='inputfile',
	help='file contain candidate CNVs'
)


ap.add_argument(
	'-r',
	'--rate',
	type=float,
	default='0.5',
	metavar='rate of overlap',
	help='the cutoff of rate'
)



args = ap.parse_args()

#####################

def Get_two_overCNV(file1,file2,rate):
	Chr={}
	rate=float(rate)
	for line1 in file1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		#if line1_list[5] != sample: continue
		if "chr" not in line1_list[0]: line1_list[0]="chr"+line1_list[0]
		ty=line1_list[4]

		#if "INS" in ty :line1_list[2]=str(int(line1_list[1])+int(line1_list[3])-1)

		li="\t".join([line1_list[1],line1_list[2],line1_list[3],ty])
		if line1_list[0] not in Chr.keys():
			Chr[line1_list[0]]=li
		else:
			Chr[line1_list[0]]=Chr[line1_list[0]]+"\n"+li
		
	for line2 in file2:
		line2=line2.strip("\n")
		line2_list=line2.split("\t")
		if line2_list[0] not in Chr.keys(): continue
		file1_list=Chr[line2_list[0]].split("\n")


		if line2_list[4] == "INS" :
			lable=0
			for cnv in file1_list:			
				cnv_list=cnv.split("\t")
				if cnv_list[3] != "INS":continue
				dis=abs(int(cnv_list[0])-int(line2_list[1]))+1
				if dis <= 200 :
					#print("{}\t{}\tTrue\t1".format(line2,dis))
					lable=1
					break
				else:
					continue
			if lable==1:
				print("{}\t{}\tTrue\t1".format(line2,dis))
			else:
				print("{}\t-\tFalse\t0".format(line2))

		else:
			label=0
			for cnv in file1_list:
				cnv_list=cnv.split("\t")
				if cnv_list[3] == "INS":continue
				if cnv_list[3] != line2_list[4]:continue

				pos_l=int(line2_list[1] )
				pos_r=int(line2_list[2])
				pos_l0=int(cnv_list[0])
				pos_r0=int(cnv_list[1])
				if pos_l > pos_r0 or pos_r < pos_l0:
					continue
				else:
					arr=sorted([pos_l,pos_r,pos_l0,pos_r0])
					overlab=arr[2]-arr[1]+1
					over_rate=overlab/(pos_r-pos_l+1)
					over_rate0=overlab/(pos_r0-pos_l0+1)
					if over_rate>=rate :
						label=1
						#print("{}\t{}\t{}\tTure\t1".format(line2,cnv,over_rate))
						break
					else:continue
			if label==1:
				print("{}\t{}:{}\tTrue\t1".format(line2,over_rate,over_rate0))
			else:
				print("{}\t-\tFalse\t0".format(line2))


if __name__ == "__main__":
	f1=open(args.goldCNV,"r")
	f2=open(args.inputfile,"r")
	Get_two_overCNV(f1,f2,args.rate)			
