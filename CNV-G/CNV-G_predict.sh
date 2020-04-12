#!/bin/bash

usage() {
    echo "Usage:"
    echo "  $0 [-i BAMFILE] [-b BASFILE] [-e BEDFILE] [-m MODEL] [-p PYTHON] [-o OUTDIR] [-n SAMPLENAME] [-c CODE_PATH] "
    echo "Description:"
    echo "    BAMFILE, the path of *.bam"
    echo "    BASFILE, the path of *.bas"
    echo "    BEDFILE, the path of *.bed"
    echo "    MODEL, the path of machine learning model [RF,GBC or SVM]"
    echo "    PYTHON, the path of python"
    echo "    OUTDIR, the path of outdir"
    echo "    SAMPLENAME, the prefix of outputfile"
    echo "    CODE_PATH, the path of CNV-P code"
    exit -1
}


while getopts i:b:e:p:m:o:n:c:h OPT; do
    case $OPT in
        i) BAMFILE="$OPTARG";;
        b) BASFILE="$OPTARG";;
        e) BEDFILE="$OPTARG";;
	p) PYTHON="$OPTARG";;
        m) MODEL="$OPTARG";;
	o) OUTDIR="$OPTARG";;
	n) SAMPLENAME="$OPTARG";;
	c) CODE_PATH="$OPTARG";;
	s) CNVCALLER="$OPTARG";;
        h) usage;;
        ?) usage;;
    esac
done


echo $BAMFILE
echo $BASFILE
echo $BEDFILE
echo $MODEL
echo $PYTHON
echo $OUTDIR
echo $SAMPLENAME
echo $CODE_PATH

##################
echo "Runing feature extraction ......"
$PYTHON $CODE_PATH/CNV-G/script/Main_Feat_Extra.py -bed $BEDFILE -bam $BAMFILE -bas $BASFILE -o $OUTDIR/$SAMPLENAME -s $SAMPLENAME 

echo "Predicting ......"
$PYTHON $CODE_PATH/CNV-G/script/CNV-G_Predict.py -m $CODE_PATH/CNV-G/model/$MODEL.train_model.m -f $OUTDIR/$SAMPLENAME.feature.txt -ft txt -o $OUTDIR

paste $BEDFILE $OUTDIR/pre.prop.txt > $OUTDIR/$SAMPLENAME.pre.prop.txt

echo "Removes the temporary file ......"
rm $OUTDIR/pre.prop.txt

echo"All jobs done."
