import sys
import gzip

#Defind the USAGE
import argparse

class CapitalisedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
	def add_usage(self, usage, actions, groups, prefix=None):
		if prefix is None:
			prefix = 'Usage: '
			return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

ap = argparse.ArgumentParser(formatter_class=CapitalisedHelpFormatter)


ap.add_argument(
	'-vcf',
	'--vcffile',
	type=str,
	required =True,
	default=None,
	metavar='vcffile',
	help='unzip vcffile from the output of CNVcaller(breakdancer/CNVnator/delly/lumpy/pindel/manta)'
)

ap.add_argument(
	'-soft',
	'--softname',
	type=str,
	default=None,
	required =True,
	metavar='softname',
	help='the name of CNVcaller,must be one of breakdancer/CNVnator/delly/lumpy/pindel/manta'
)

args = ap.parse_args()

###################


def bp_bed(f1):
	for line1 in f1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		if '#' in line1_list[0]:continue
		if line1_list[6] != 'DEL' and line1_list[6] != 'INS' and line1_list[6] != 'DUP' :continue
		# length
		if abs(float(line1_list[7])) < 100 :continue

		line1_list[7]=str(abs(int(line1_list[7])))
		out='\t'.join([line1_list[0],line1_list[1],line1_list[4],line1_list[7],line1_list[6]])
		print(out)

def cn_bed(f1):
	for line1 in f1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		if '#' in line1_list[0]:continue
		if line1_list[0] != 'deletion' and  line1_list[0] != 'duplication':continue
		#filter
		if float(line1_list[8]) >= 0.5 :continue
		# length
		if float(line1_list[2]) < 100 :continue

		if line1_list[0] == 'deletion':line1_list[0]= 'DEL'
		else: line1_list[0]= 'DUP' 
		pos_list=line1_list[1].split(':')
		chrom=pos_list[0]
		sta=pos_list[1].split('-')[0]
		end=pos_list[1].split('-')[1]
		out='\t'.join([chrom,sta,end,line1_list[2],line1_list[0]])
		print(out)


def delly_bed(f1):
	for line1 in f1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		if '#' in line1_list[0]:continue
		if 'DUP' not in line1_list[4] and 'DEL' not in line1_list[4] and 'INS' not in line1_list[4]:continue
		SV=line1_list[7].split(';')
		info_dict={}
		for info in SV:
			if("=" not in info):continue
			info_list=info.split('=')
			info_dict[info_list[0]]=info_list[1]

		svtype=info_dict["SVTYPE"]
		end=info_dict["END"]
		length=int(end)-int(line1_list[1])+1
		if svtype == 'INS':
			length= info_dict["INSLEN"]
		# length
		if float(length) < 100 :continue

		out='\t'.join(map(str,[line1_list[0],line1_list[1],end,length,svtype]))

		print(out)

def Lumpy_bed(f1):
	for line1 in f1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		if '#' in line1_list[0]:continue
		if 'DUP' not in line1_list[4] and 'DEL' not in line1_list[4] and 'INS' not in line1_list[4]:continue
		SV=line1_list[7].split(';')
		info_dict={}
		for info in SV:
			if("=" not in info):continue
			info_list=info.split('=')
			info_dict[info_list[0]]=info_list[1]

		svtype=info_dict["SVTYPE"]
		end=info_dict["END"]
		length=int(end)-int(line1_list[1])+1
		if svtype == 'INS':
			length= info_dict["SVLEN"]
		# length	
		if float(length) < 100  : continue	

		out='\t'.join(map(str,[line1_list[0],line1_list[1],end,length,svtype]))

		print(out)

def pindel_bed(f1):
	for line1 in f1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		if '#' in line1_list[0]:continue
		if 'DUP' not in line1_list[7] and 'DEL' not in line1_list[7] and 'INS' not in line1_list[7]:continue
		SV=line1_list[7].split(';')
		n_list=[]
		for i in SV:
			i_list=i.split('=')
			n_list.append(i_list)
		n_dict=dict(n_list)
		svtype=n_dict["SVTYPE"]
		if 'DUP' in svtype : svtype = 'DUP'
		elif 'DEL' in svtype : svtype = 'DEL'
		else: svtype='INS'
		end=n_dict["END"]
		length=int(end)-int(line1_list[1])+1
		if svtype == 'INS':
			length= int(n_dict["SVLEN"])
		if float(length) < 100 :continue
		out='\t'.join(map(str,[line1_list[0],line1_list[1],end,length,svtype]))

		print(out)

def manta_bed(f1):
	for line1 in f1:
		line1=line1.strip("\n")
		line1_list=line1.split("\t")
		if '#' in line1_list[0]:continue
		if 'DUP' not in line1_list[7] and 'DEL' not in line1_list[7] and 'INS' not in line1_list[7]:continue
		SV=line1_list[7].split(';')

		n_dict={}
		for info in SV:
			if("=" not in info):continue
			info_list=info.split('=')
			n_dict[info_list[0]]=info_list[1]

		svtype=n_dict["SVTYPE"]
		if "SVLEN" not in n_dict.keys():continue

		end=n_dict["END"]
		length=int(end)-int(line1_list[1])+1
		if svtype == 'INS':
			length= int(n_dict["SVLEN"])

		#length
		if float(length) < 100 :continue

		out='\t'.join(map(str,[line1_list[0],line1_list[1],end,length,svtype]))

		print(out)


if __name__ == "__main__":
	f1=open(args.vcffile,"r")
	if args.softname == 'breakdancer':
		bp_bed(f1)
	elif args.softname == 'CNVnator':
		cn_bed(f1)
	elif args.softname == 'Delly':
		delly_bed(f1)
	elif args.softname == 'Lumpy':
		Lumpy_bed(f1)
	elif args.softname == 'Pindel':
                pindel_bed(f1)
	elif args.softname == 'Manta':
		manta_bed(f1)
	else:print('error')
	
