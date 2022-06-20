from random import sample
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
def pareto_random_sample(shape,num_sample):
  
  
    si = (shape - 1) / shape
   
    sample = np.linspace(start = si, stop = 6, num=num_sample)
    pdf = np.array([stats.pareto.pdf(x=sample, b=shape,loc=0,scale=si)])
    normalized_pdf = pdf[0]/np.sum(pdf[0])
    return np.random.choice(a = sample, size =num_sample,replace = True,p=normalized_pdf)
