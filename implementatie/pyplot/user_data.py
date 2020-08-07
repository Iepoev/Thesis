import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'size' : 6}

matplotlib.rc('font', **font)





# Load file
data = np.load("/home/iepoev/Git/Unief/Thesis/implementatie/data/processed/karolina_sequence.npy")





fig, axs = plt.subplots(4,3)

axs[0,0].set_title('ms')
axs[0,0].plot(data[:,0]/60000,data[:,1], linewidth=0.5) # ms

axs[0,1].set_title('HR')
axs[0,1].plot(data[:,0]/60000,data[:,2], linewidth=0.5) # HR

axs[0,2].set_title('HRV')
axs[0,2].plot(data[:,0]/60000,data[:,3], linewidth=0.5) # HRV (weighted moving average)

axs[1,0].set_title('SDNN')
axs[1,0].plot(data[:,0]/60000,data[:,4], linewidth=0.5) # SDNN

axs[1,1].set_title('SDSD')
axs[1,1].plot(data[:,0]/60000,data[:,5], linewidth=0.5) # SDSD

axs[1,2].set_title('pNN50')
axs[1,2].plot(data[:,0]/60000,data[:,6], linewidth=0.5) # pNN50

axs[2,0].set_title('RMSSD')
axs[2,0].plot(data[:,0]/60000,data[:,7], linewidth=0.5) # rMSSD

axs[2,1].set_title('HF Power (60s epoch)')
axs[2,1].plot(data[:,0]/60000,data[:,8], linewidth=0.5) # 60s VLF

axs[2,2].set_title('VLF Power (300s epoch')
axs[2,2].plot(data[:,0]/60000,data[:,9], linewidth=0.5) # 60s LF

axs[3,0].set_title('LF Power (300s epoch')
axs[3,0].plot(data[:,0]/60000,data[:,10], linewidth=0.5) # 60s HF

axs[3,1].set_title('LF/HF ratio (300s epoch)')
axs[3,1].plot(data[:,0]/60000,data[:,11], linewidth=0.5) # 60s LF/HF

axs[3,2].set_title('category')
axs[3,2].plot(data[:,0]/60000,data[:,12], linewidth=0.5) # 300s VLF

fig.tight_layout(pad=1.5)

plt.savefig("user_data.png", bbox_inches='tight', dpi=600)




