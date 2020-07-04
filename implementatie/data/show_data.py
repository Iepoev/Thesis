import matplotlib.pyplot as plt
import numpy as np

data = np.load('data.npy')

plt.plot(data[:,0]/60000,data[:,1], linewidth=0.5) # ms
# plt.plot(data[:,0]/60000,data[:,2], linewidth=0.5) # HR
# plt.plot(data[:,0]/60000,data[:,3], linewidth=0.5) # HRV (weighted moving average)
# plt.plot(data[:,0]/60000,data[:,4], linewidth=0.5) # SDNN
# plt.plot(data[:,0]/60000,data[:,5], linewidth=0.5) # SDSD
# plt.plot(data[:,0]/60000,data[:,6], linewidth=0.5) # NN50
# plt.plot(data[:,0]/60000,data[:,7], linewidth=0.5) # rMSSD
plt.ylabel('dinken')
plt.savefig('demo_.png', bbox_inches='tight', dpi=300)