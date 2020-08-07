import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'size'   : 6}

matplotlib.rc('font', **font)

fig, axs = plt.subplots(1,3,figsize=(9,3))
axs[0].set_title('Heart Rate')
axs[0].boxplot([

[ 78.201,  99.909,  59.94 , 109.655,  81.263, 104.933,  73.492,
        89.045,  86.142,  76.525,  91.274,  90.36 ,  87.434, 111.156,
        94.074,  83.728,  73.718,  85.221, 109.91 ,  86.674, 108.004,
        74.464],
[103.428, 117.974,  99.89 , 124.572,  99.691, 124.579, 101.734,
       105.989, 105.246, 111.382, 118.66 , 127.737, 123.277, 147.928,
       113.45 , 116.652,  91.972, 108.21 , 138.093, 108.569, 135.5  ,
        95.078],
[133.139, 132.512, 132.658, 153.839, 125.954, 142.045, 118.689,
       125.12 , 121.496, 150.2  , 156.654, 153.45 , 158.651, 186.645,
       127.702, 138.426, 108.42 , 120.018, 163.766, 126.05 , 168.302,
       119.286],
[182.823, 176.216, 182.794, 183.607, 171.683, 189.759, 175.395,
       178.278, 172.471, 180.883, 186.251, 175.153, 180.109, 186.752,
       178.619, 175.233, 176.732, 182.348, 190.104, 186.215, 183.392,
       177.504],
])
axs[0].set_xticklabels(["Rest HR", "Max HR (50W)", "Max HR (100W)", "Max HR"],rotation=15)
axs[0].set_aspect('auto')
axs[0].set_ylim(50,200)


axs[1].set_title('Calories expended during stage')
axs[1].boxplot([

[22., 19., 20.,  8., 23., 14., 21., 24., 25., 23., 12.,  9.,  8.,
        6., 18., 21., 32., 22., 12., 23.,  7., 23.],
[42., 46., 35., 38., 45., 43., 55., 54., 49., 31., 28., 34., 27.,
       15., 49., 45., 58., 62., 26., 59., 25., 56.],
[20., 20., 10., 12., 21., 20., 20., 20., 12., 17., 12., 10., 23.,
       10., 21., 20., 21., 24., 20., 15., 11., 27.],
])
axs[1].set_xticklabels(["60% HR", "80% HR", "Max HR"],rotation=15)
axs[1].set_aspect('auto')
axs[1].set_ylim(0,80)



axs[2].set_title('Baeke scores')
axs[2].boxplot([
[1.875, 1.75 , 1.75 , 1.875, 1.75 , 1.375, 1.5  , 1.875, 1.75 ,
       1.75 , 1.75 , 1.75 , 2.125, 2.   , 1.25 , 1.875, 2.75 , 1.125,
       1.375, 1.875, 1.625, 1.25 ],
[2.5 , 3.5 , 2.25, 1.  , 3.75, 3.5 , 2.75, 3.5 , 3.25, 2.75, 2.  ,
       2.25, 2.  , 2.75, 4.75, 3.  , 3.25, 3.75, 1.75, 1.5 , 1.5 , 2.  ],
[3.  , 2.25, 3.5 , 3.  , 2.5 , 3.75, 2.75, 3.  , 3.  , 2.75, 3.  ,
       3.  , 3.5 , 3.25, 4.  , 3.  , 3.25, 3.25, 2.75, 3.25, 3.  , 4.  ],
])
axs[2].set_xticklabels(["Work", "Sport", "Leisure"],rotation=15)
axs[2].set_aspect('auto')
axs[2].set_ylim(0,5)


plt.savefig("user_profile_hr.png", bbox_inches='tight', dpi=200)


