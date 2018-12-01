import xml.etree.cElementTree as ET 
import pickle
import os
import re
# Using Elbow methord to reduce average distance between centroid and cluster
import matplotlib.pyplot as plt
import pandas as pd # For Data Analytics
from sklearn.cluster import KMeans
import numpy
from numpy.linalg import inv

#===================-- SET DIRECTORY NAME --=================================
folder_to_data_folder_path='Data'
#============================================================================


def Tmat_cal(path,filename):
	filename2='Nmat_Kmat/'+filename+'_Nmat.pkl'
	with open(filename2,'rb') as f:
		Nmat=pickle.load(f)
	filename2='Nmat_Kmat/'+filename+'_Kmat.pkl'
	with open(filename2,'rb') as f:
		Kmat=pickle.load(f)

	self_trig=0.00001	
	Tmat=numpy.matrix([[self_trig,2],[2,self_trig]])
	R=numpy.matrix([[0.01],[0.01]])
	result=inv(Nmat)*(Kmat-(Nmat*R))
	X=(result[0,0]-(self_trig*Kmat[0,0]))/Kmat[1,0]
	Y=(result[1,0]-(self_trig*Kmat[1,0]))/Kmat[0,0]
	Tmat=numpy.matrix([[self_trig,X],[Y,self_trig]])
	
	times_loop_run=100
	Tmat1=Tmat
	while times_loop_run>0:
		if numpy.linalg.eig(Nmat*Tmat)<1 and X>0 and Y>0:
			break
		else:
			self_trig=self_trig/10
			X=(result[0,0]-(self_trig*Kmat[0,0]))/Kmat[1,0]
			Y=(result[1,0]-(self_trig*Kmat[1,0]))/Kmat[0,0]
			Tmat=numpy.matrix([[self_trig,X],[Y,self_trig]])	
		times_loop_run-=1
	
	filename2='Tmat/'+filename+'_Tmat.pkl'
	with open(filename2,'wb') as f:
		pickle.dump(Tmat,f)
	print "---------------------",filename,"--------------------------"
	#const=numpy.matrix([[1,0],[0,1]])
	#print numpy.linalg.inv(const-Nmat*Tmat)*Nmat*R
	#print Kmat
	print Tmat
	
def main():
	path=os.getcwd()+'/'+folder_to_data_folder_path
	arr = os.listdir(path)
	if((os.path.isdir(os.getcwd()+"/Nmat_Kmat"))==False):
		print "Run Nmat_Kmat.py"
		return
	if((os.path.isdir(os.getcwd()+"/Tmat"))==False):	
		os.mkdir("Tmat")
	for files in arr:
		Tmat_cal(path+'/'+files,files)
main()
