#!/bin/bash

usage() {
    echo "Usage:"
    echo "  $0 [-i BAMFILE] [-b BASFILE] [-v VCFFILE] [-m MODEL] [-p PYTHON] [-o OUTDIR] [-n SAMPLENAME] [-c CODE_PATH] [-s CNVCALLER]"
    echo "Description:"
    echo "    BAMFILE, the path of *.bam"
    echo "    BASFILE, the path of *.bas"
    echo "    VCFFILE, the path of *.vcf"
    echo "    MODEL, the path of machine learning model [RF,GBC or SVM]"
    echo "    PYTHON, the path of python"
    echo "    OUTDIR, the path of outdir"
    echo "    SAMPLENAME, the prefix of outputfile"
    echo "    CODE_PATH, the path of CNV-P code"
    echo "    CNVCALLER, the name of CNVcaller [breakdancer,Delly,Lumpy,Manta or Pindel]"
    exit -1
}


while getopts i:b:v:p:m:o:n:c:s:h OPT; do
    case $OPT in
        i) BAMFILE="$OPTARG";;
        b) BASFILE="$OPTARG";;
        v) VCFFILE="$OPTARG";;
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
echo $VCFFILE
echo $MODEL
echo $PYTHON
echo $OUTDIR
echo $SAMPLENAME
echo $CODE_PATH
echo $CNVCALLER

##################
echo "Data Procecing ......"
$PYTHON $CODE_PATH/script/getrowCNVbed.py -vcf $VCFFILE -soft $CNVCALLER > $OUTDIR/$SAMPLENAME.$CNVCALLER.row.bed

$PYTHON $CODE_PATH/script/Remove_Nregion.py -N $CODE_PATH/script/N.region_hg19 -C $OUTDIR/$SAMPLENAME.$CNVCALLER.row.bed > $OUTDIR/$SAMPLENAME.$CNVCALLER.fil.bed

$PYTHON $CODE_PATH/script/merone_overlabCNV.py -b $OUTDIR/$SAMPLENAME.$CNVCALLER.fil.bed |grep -v INS |sed 's/DUP/1/' | sed 's/DEL/0/g' > $OUTDIR/$SAMPLENAME.$CNVCALLER.fil.mer.bed

echo "Runing feature extraction ......"
$PYTHON $CODE_PATH/script/Main_Feat_Extra.py -bed $OUTDIR/$SAMPLENAME.$CNVCALLER.fil.mer.bed -bam $BAMFILE -bas $BASFILE -o $OUTDIR/$SAMPLENAME.$CNVCALLER -s $SAMPLENAME 

echo "Predicting ......"
$PYTHON $CODE_PATH/script/CNV-P_Predict.py -m $MODEL -f $OUTDIR/$SAMPLENAME.$CNVCALLER.feature.txt -ft txt -o $OUTDIR 

paste $OUTDIR/$SAMPLENAME.$CNVCALLER.fil.mer.bed $OUTDIR/pre.prop.txt > $OUTDIR/$SAMPLENAME.$CNVCALLER.pre.prop.txt

echo "Removes the temporary file ......"
rm $OUTDIR/pre.prop.txt
rm $OUTDIR/$SAMPLENAME.$CNVCALLER.row.bed
rm $OUTDIR/$SAMPLENAME.$CNVCALLER.fil.bed

echo"All jobs done."
