To run the code, simply execute main.py.
1. The directory RowLessThanOne contains 25 graphs for random N and T, for which row(NT) < 1.
    The values of the entries in T were set to be between 0 and 0.01.
2. The directory RowNotLessThanOne contains 25 graphs for random N and T, for which row(NT) < 1 only for some values of NT.
    The values of the entries in T were set to be between 0.01 and 0.02.
    Please note that the graphs were plotted only for those points which satisfied row(NT) < 1.
3. If we set values of elements of T to be more than 0.02, the value of row(NT) becomes greater than one for all N.
    In that case, Kc_infinity would tend towards infinity and thus can not be plotted.
