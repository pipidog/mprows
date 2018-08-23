# Multi-Processing on Row Data
This package is simply a python decorator to help your perform multiprocessing based on row data. This is especially useful if your are trying to clean large size data.

Suppose you have a numpy array called "data" (can be any dimension) and you want to repeat some operation on each row (i.e 0-th dimension). This decorator can help you painlessly perform the operation using multiprocessing.

The idea is simple. The decorator will automatically split your data into several subsets (by rows) and run the function using multiprocessing. Once it is done, the code will combine all results and return the modified numpy array. 

# Requirements
To use it, you must install the follow python packages from pip install  
**numpy, pathos, itertools**

# Installation:

**pip install mprows** 

# Usage:
## Function Format
when you build your own function, it must built based in this form:

    MyFunc(data, par={'par1': value1, 'par2': value2})

        * function name is arbitary

        * function must contain only two arguemnts, one is called "data", (i.e your data, a numpy array) while the other one is called "par" (a dict that contains all the other arguments of your function. It will be fixed in the multiprocessing procedure.)
 
        * This decorator can only decorate a "function", not a method in a class. If you want to perform multiprocessing a in method, you can define a function in the method which wraps all the code of your method and use the decorator on it.  

        * The output of your function should be another numpy array which has the same number of rows.  

        * since this code will split your data based on row, you must make sure that the operation is "row independent".

## Example
You must first import mprows:  

**from mprows import mprows**   

Then you can simply program your own function and use mprows as a decorator for multiprocessing. 

To multiprocess a function:
<p align="center">
<img src="./img/func.png">
</p>  

To multiprocess a method in a class:
<p align="center">
<img src="./img/class.png">
</p>