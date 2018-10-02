import numpy as np 
from itertools import repeat
from pathos.multiprocessing import ProcessingPool as Pool
import pandas as pd

class mprows:
    ''' 
    This class is used as a decorator in front of a data processing function. 
    Suppose you have a numpy array called "data" (can be any dimension) and you 
    want to repeat some operation on each row (i.e 0th dimension) independently, 

    This decorator can help you painlessly perform the operation using multiprocessing.

    The idea is simple, the decorator will automatically split the data into several 
    subsets (by rows) and run the function using multiprocessing. Once it is done, 
    the code will combine all results into a single numpy array. 

    Usage:
    1). when you build your own function, you must build your function in this form:

        MyFunc(data, par={'par1': value1, 'par2': value2})
    
            1: function name can ba anything
            2: this function must contain only two arguemnts, one is called "data"
                and the other one is called "par"
            3: "data" is your numpy array. "par" is a dict which contains all the 
                other arguments of your function that will be fixed in the multiprocessing 
                procedure. 
            4. This decorator can only decorate a "function", not a method in a class. 
                If you want to perform multiprocessing a in method, you can define a 
                function in the method which wraps all the code of your method and 
                use the decorator on it.  

    2). since this code will split your data based on row, you must make sure that
        the operation is "row independent"..
    '''
    def __init__(self, n_proc =1):
        self.n_proc = n_proc
    def _multiproc_data_split(self, data):
        # split data for multicore processing
        proc_data = []
        batch_size = int(len(data)/self.n_proc)
        for n in range(self.n_proc):
            if (type(data) == type(np.array([0]))) or (type(data) == type([])):
                if n!=self.n_proc-1:
                    proc_data.append(data[n*batch_size:(n+1)*batch_size])
                else:
                    proc_data.append(data[n*batch_size:])   
            elif type(data) == type(pd.DataFrame([0])):
                if n!=self.n_proc-1:
                    proc_data.append(data.iloc[n*batch_size:(n+1)*batch_size,:])
                else:
                    proc_data.append(data.iloc[n*batch_size:,:])                   
        return proc_data

    def __call__(self, func):
        def decorator(data, par):
            if (type(data)!=type(np.zeros(3))) and (type(data) != type(pd.DataFrame([0]))) and (type(data)!=type([])): 
                raise TypeError('data type must be a list, a numpy array or a pandas DataFrame!')

            if self.n_proc == 1:
                print(' processing data in single-core mode')
                result = func(data, par)
            else:
                print(' processing data in %d-core mode' % self.n_proc)
                pool = Pool()
                data = self._multiproc_data_split(data)
                result = pool.map(func, data, repeat(par))
                if type(result[0]) == type(np.array([0])): 
                    result = np.concatenate(result, axis = 0)   
                elif type(result[0]) == type(pd.DataFrame([0])):
                    result = pd.concat(result, axis = 0)
                elif type(result) == type([]):
                    res = []
                    [res.extend(tmp) for tmp in result]
                    result = res
                else:
                    print('mprows: output data structure of the given '+
                        'function is not recognized. Return a list containing results of each process !')
            return result
        return decorator           
