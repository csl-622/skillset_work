#                              Skillset_work
# Project:-
#  Analyze Knowledge Building Scenario's and Optimize it for better Knowledge Building

#                 A guide to Run Components of the Project 


Begin:- 

Initially Place Website Data in Data folder

Components:-

prog.py :- 

1.) For Each website, it calculates It's Contributor's percentage according to SPECIALITY ( Total SUM UP to 100% )

2.) For Each User calculates it's category wise Contribution 

3.) The output is stored in Results in text format and as well as PKL


Nmat_Kmat.py :-

1.) First get User Data along with their contribution amount and domain from prog.py
    i.e Run prog.py => Store Data in pkl format in Results

2.) Now Run Nmat_Kmat.py which stores its results in Nmat_Kmat folder
    Nmat contains user Distribution based on their contribution domain calculated through K-means clustering algorithm.
    K Matrix contains knowledge generated across Domain's

Tmat.py:-

1.) First run Nmat_Kmat.py to store Nmatrix and K matrix in pickle

2.) Run Tmat.py which calculates the Triggering happening across User's of Different Category
