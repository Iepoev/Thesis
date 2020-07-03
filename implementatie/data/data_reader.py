from functools import reduce
import numpy as np
import math
import operator

resting_hr = 220
max_hr = 0
current_hr = 0
current_hrv = 0
prev_ms = 0

ms_window = []
hr_window = []
total_ms = 0

# data matrix: 1 row is 1 HRV measurement
# ms since last beat
# user max heart rate
# user resting heart rate
# user heart recovery rate (60s)
# HRV laatste 5 beats
# HRV laatste 20 beats
# HRV laatste  beats
# HRV LF is een exercise indicator
# Parasympathic activity (Ln rMSSD)
# Current Heart Rate (10s window)
# Current Heart Rate (30s window)
# Current Heart Rate (60s window)
# Current Heart Rate (120s window)
# Heart Recovery rate (60s) [@Hug2014]


A = np.empty((0,4), dtype=float)

with open('raw/2020-07-02 22-23-08 - poef - interval.txt', 'r') as file:
  prev_ms = int(file.readline())

  for l in file:

    ms = int(l)
    total_ms += ms
    ms_diff = abs(prev_ms - ms)
    if ms_diff <= 100 or ms_diff <= current_hrv * 2:
      print(f"{prev_ms - ms}, {current_hrv}")
      ms_window.append(ms)

      if len(ms_window) == 10: #

        #60000 ms in 1 minute
        current_hr = 60000 / np.average(ms_window)
        hr_window.append(current_hr)

        # current hrv is averaged over last 10 beats
        current_hrv = np.average(list(map(lambda x, y: abs(x-y), ms_window[1:], ms_window[:-1])))

        # max_hr is een momentopname
        if current_hr > max_hr:
          max_hr = current_hr

        # if there is enough data (60 beats), calculate a smoothened HR
        if len(hr_window) == 60:
          smoothened_hr = sum(hr_window[-60:])/len(hr_window[-60:])

          # resting hr can be measured over a longer period of time
          if smoothened_hr < resting_hr:
            resting_hr = current_hr
        
          hr_window.pop(0)

        prev_ms = ms_window.pop(0)

      newrow = [total_ms, ms, current_hr, current_hrv]
      A = np.append(A, [newrow], axis=0)
    else:
      print(f">>>>>>>> {prev_ms - ms}")

    prev_ms = ms

user = [resting_hr, max_hr]

print(user)
#print(A)
np.save('data.npy', A)