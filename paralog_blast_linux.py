import os
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
filelist=os.listdir()
filelist.remove('acrb.fasta')
select_seq=[]
select_id=[]
for i in filelist:
    allseq=[seq_record.seq for seq_record in SeqIO.parse(i,'fasta')]
    allid=[seq_record.id for seq_record in SeqIO.parse(i,'fasta')]
    os.system('makeblastdb -in '+i+' -dbtype prot -out dbname')
    comm='blastp -query acrb.fasta -out result.txt -db dbname -evalue 1e-2 -outfmt 6'
    os.system(comm)
    result=pd.read_table('result.txt')
    for k in range(len(result)):
        if result.iat[k,2]>80:
            select_id.append(result.iat[k,1])
            select_seq.append(allseq[allid.index(result.iat[k,1])])
#write fasta file
current_gene=()
fastafile=()
for i in range(len(select_id)):
    current_gene=(SeqRecord(select_seq[i],id=select_id[i]),)
    fastafile=fastafile+current_gene
SeqIO.write(fastafile,'result.fasta','fasta')