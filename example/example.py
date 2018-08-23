'''
this code shows how to use mprows to multiprocessing your function
'''
import numpy as np
from mprows.mprows import mprows

task = 'class'  # 'class' / 'func'
par = {'op':'add', 'const': 5}
n_proc = 5

# ==================================
data = np.ones((1000,3))
if task == 'class':
    class test:
        def __init__(self, n_proc):
            self.n_proc = n_proc
        def foo(self, data, par = {'op':'add', 'const':2}):
            # can only decorate a function, not a method. so please wrap it. 
            @mprows(n_proc = self.n_proc)
            def wrapper(data, par):
                if par['op'] == 'add':
                    data = data+par['const']
                elif par['op'] == 'mul':
                    data = data*par['const']
                return data
            return wrapper(data, par)        
    data = test(n_proc = n_proc).foo(data, par)
elif task == 'func':
    @mprows(n_proc = n_proc)
    def foo(data, par = {'op':'add', 'const':2}):
        if par['op'] == 'add':
            data = data+par['const']
        elif par['op'] == 'mul':
            data = data*par['const']
        return data
    data = foo(data, par)

print(data)