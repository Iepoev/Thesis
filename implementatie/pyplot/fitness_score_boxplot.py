import numpy as np
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()
ax1.set_title('Fitness scores')
ax1.boxplot([[102.06,
103.73,
106.03,
131.93,
133.15,
135.44,
139.30,
139.32,
139.43,
143.36,
153.84,
155.32,
160.43,
163.75,
171.80,
126.77,
56.95,
76.84,
80.82,
93.16,
101.65,
108.10],

[56.95,
76.84,
80.82,
93.16,
101.65,
108.10],

[102.06,
103.73,
106.03,
131.93,
133.15,
135.44,
139.30,
139.32,
139.43,
143.36,
153.84,
155.32,
160.43,
163.75,
171.80]
])
ax1.set_xticklabels(["Overall", "female", "Male"],fontsize=8)
ax1.set_aspect(0.008)


plt.savefig("fitness_score_boxplot.png", bbox_inches='tight', dpi=200)


