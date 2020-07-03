import matplotlib.pyplot as plt
import numpy as np

data = np.load('data.npy')

#plt.plot(data[:,0]/60000,data[:,1], linewidth=0.5)
plt.plot(data[:,0]/60000,data[:,2], linewidth=0.5)
plt.plot(data[:,0]/60000,data[:,3], linewidth=0.5)
plt.ylabel('dinken')
plt.savefig('demo_.png', bbox_inches='tight', dpi=300)