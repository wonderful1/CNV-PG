from sklearn.metrics import roc_curve, auc ,precision_recall_curve
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from itertools import cycle
import sys


import argparse
#Defind the USAGE
class CapitalisedHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
	def add_usage(self, usage, actions, groups, prefix=None):
		if prefix is None:
			prefix = 'Usage: '
			return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)

ap = argparse.ArgumentParser(formatter_class=CapitalisedHelpFormatter)

ap.add_argument(
	'-m',
	'--model',
	type=str,
	default=None,
	required=True,
	metavar='model',
	help='path to model'
)

ap.add_argument(
	'-f',
	'--feature',
	type=str,
	default=None,
	required=True,
	metavar='features',
	help='file provides features'
)

ap.add_argument(
	'-ft',
	'--file_type',
	type=str,
	default="txt",
	metavar='file_type',
	help='the format of input file'
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


##### get X Y to predict 
def GetRawdata(feat_f,file_type):
	if file_type == "np":
		x1=np.load(feat_f)
		print(x1.shape)
	else:
		feat_f = open(feat_f,"r")
		data_list1=[]
		col4_li=[]
		for line0 in feat_f:
			line0=line0.strip("\n")
			num=line0.split("\t")
			if num[0]=="space":feat_labels=num[3:20];continue
			col4=num[0:4]
			num=num[3:20]
			data_list1.append(num)
			col4_li.append(col4)
		x1 = np.array(data_list1)
		info=np.array(col4_li)
		print(x1.shape)
		print(info.shape)
		
	return x1,info



if __name__ == "__main__":
	outdir=args.output
	mod=args.model
	print("Get x,y ....")
	x,info=GetRawdata(args.feature,args.file_type)
	print("Loading mode and predict.... ")
	yscore_dict={}
	Classifier = joblib.load(mod)
	y1_pre_score=Classifier.predict_proba(x)
	yscore_dict[mod]=y1_pre_score
		
	y_pre=Classifier.predict(x)
	yp=np.array(y_pre)
	ys=np.array(y1_pre_score[:,1])
	print(yp.shape,ys.shape)
	#y:true #yp:predict #ys:score
	out=np.vstack((yp,ys)).T
		
#	out1=np.vstack(np.array(y_pre),np.array(y1_pre_score[:,1]))
#	out=np.vstack(out0,out1)
	np.savetxt(outdir +"/" + "pre.prop.txt",out,fmt="%s")
	
