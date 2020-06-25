import numpy as np


window = []

resting_hr = 220
max_hr = 0
current_hr = 0

# data matrix: 1 row is 1 HRV measurement
# ms since last beat
# user max heart rate
# user resting heart rate
# HRV laatste 5 beats
# HRV laatste 20 beats
# HRV laatste  beats
# HRV LF is een exercise indicator
# Parasympathic activity (Ln rMSSD)
# Current Heart Rate (10s window)
# Current Heart Rate (30s window)
# Current Heart Rate (60s window)
# Current Heart Rate (120s window)
# Max Heart Rate
# Resting Heart Rate
# Heart Recovery rate (60s) [@Hug2014]


A = np.array([[0,0,0]], dtype=int)

with open('raw/squat_warmup.txt', 'r') as fp:
  ms = fp.readline()

  window.append(ms)

  if len(window) == 10:
    current_hr = (60000 / (sum(window)/len(window)))
    if current_hr < resting_hr:
      resting_hr = current_hr
    if current_hr > max_hr:
      max_hr = current_hr
    window.pop(0)
    print('current HR {0}; current resting HR {1}; current max HR {2}'.format((60000/ms), resting_hr, max_hr))
  else:
    print('Heartbeat interval {0}ms'.format(ms))


  newrow = [ms,2,3]
  A = np.vstack([A, newrow])

print(A)
np.save('data.npy', A)