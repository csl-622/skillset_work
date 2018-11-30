#                              Skillset_work
#                                 Project :-
#  Analyze Knowledge Building Scenario's and Optimize it for better Knowledge Building

#                 A guide to Run Components of the Progect 


Begin :- 

Inditially Place Website Data in Data folder

Components :-

prog.py :- 

1.) For Every website it calculates its Contributor's percentage according to SPECIALITY ( Total SUM UP to 100% )

2.) For Each User calculates it's categeory wise Contribuition 

3.) Output is stored in Results in txt format and as well as PKL


Nmat_Kmat.py :-

1.) First get User Data along with their contribution amount and domain from prog.py
    i.e Run prog.py => Store Data in pkl format in Results

2.) Now Run Nmat_Kmat.py which stores it's result in Nmat_Kmat folder
    Nmat contains user Distribution based on their contribution domain calculated through K-means clustering algorithm.
    Kmat contains knowledge generated across Domain's

Tmat.py :-

1.) First run Nmat_Kmat.py to store Nmatrix and Kmatrix in pickle

2.) Run Tmat.py which calculates the Trigerring happening across User's of Different Category
