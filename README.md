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

**from mprows.mprows import mprows**   

Then you can simply program your own function and use mprows as a decorator for multiprocessing.  

To multiprocess a function:
```python
import numpy as np
from mprows.mprows import mprows
data = np.ones((1000,3))
@mprows(n_proc = 6) # use 6-cores to run your function
def foo(data, par={'op':'add', 'const':2}):
    if par['op'] = 'add':
        data = data+par['const']
    elif par['op'] == 'mul':
        data = data*par['const']
    return data
# now running your function will automatically use 6 cores 
data = foo(data, par = {'op':'add', 'const': 5})
```
Due to the limitation of pathos, you cannot directly decorate a method in a class, but you can decorate a method in this way:
```python
import numpy as np
from mprows.mprows import mprows
data = np.ones((1000,3))
class test:
    def __init__(self, n_proc):
        self.n_proc = n_proc 
    def foo(self, data, par={'op':'add', 'const':2} ):
        # define a wrapper in your method and decorate it
        @mprows(n_proc = self.n_proc)
        def wrapper(data, par):
            if par['op'] = 'add':
                data = data+par['const']
            elif par['op'] == 'mul':
                data = data*par['const']
            return data   
        return wrapper(data, par)
# now running your function will automatically use 6 cores 
data = test(n_proc = 6).foo(data, par = {'op':'add', 'const': 5})

```
# What are the inputs
When you design your function, you must define a variable called "data" and put all the other variables as a single dictionary call "par". "data" can be a numpy array, a pandas dataframe or a list. mprows will autometically split the data into **n_proc** pieces and pass these pieces to the function using different process. Therefore, **splitting** the data must be logical espeically when your data is a list. 
# What will be returned
When using **mprows**, you need to be catious about what will be returned. 
* **numpy** or **pandas DataFrame**   
if the return of your function is a single numpy array or a single Pandas DataFrame, mprows will automatically concatenate the resutls calculated via each process. In this regard, your function will work as usuall but processed using multiprocess. 

* **list**
In many cases, your returned data are not structured as a simple numpy array or pandas dataframe. In this regard, you can use a list as your return and mprows will return the results by using the "list.extend()" python built-in method to concatenate all results. Therefore, be caution when you use a list as your return.  
