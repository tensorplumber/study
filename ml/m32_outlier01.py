import numpy as np
a = np.array([1,2,-10,4,5,6,7,8,50,10,11])

def outliers(data_out):
    quartile_1,q2,quartile_3 = np.percentile(data_out,[25,50,75])
    print('1사분위:',quartile_1)
    print('q2:',q2)
    print('3사분위:',quartile_3)
    iqr = quartile_3 -quartile_1
    print('iqr:',iqr)
    lower_bound = quartile_1 -(iqr*1.5)
    upper_bound = quartile_3 +(iqr*1.5)
    return np.where((data_out>upper_bound)|(data_out<lower_bound))

    
outliers_loc = outliers(a)
print('이상치 위치',outliers_loc)
import matplotlib.pyplot as plt
plt.boxplot(a)
plt.show()