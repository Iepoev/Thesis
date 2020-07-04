from functools import reduce
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

class Datareader():

  def __init__(self):
    # data matrix: 1 row is 1 HRV measurement
    # ms since last beat
    # user max heart rate
    # user resting heart rate
    # user heart recovery rate (60s)
    # HRV laatste 5 beats
    # HRV laatste 20 beats
    # HRV laatste  beats
    # HRV LF is een exercise indicator
    # Parasympathic activity (Ln self.rMSSD)
    # Current Heart Rate (10s window)
    # Current Heart Rate (30s window)
    # Current Heart Rate (60s window)
    # Current Heart Rate (120s window)
    # Heart Recovery rate (60s) [@Hug2014]

    self.resting_hr = 220
    self.max_hr = 0
    self.current_hr = 0
    self.current_hrv = 0
    self.prev_ms = 0
    self.sdnn = 0
    self.sdsd = 0
    self.nn50 = 0
    self.rmssd = 0

    self.ms_10s_window = []
    self.ms_60s_window = []
    self.ms_120s_window = []
    self.ms_300s_window = []
    self.total_ms = 0


  def save_to_npy(self, data, fname="data.npy"):
    np.save(fname, data)


  def draw(self, data, input_fname="data.npy", output_fname="graph.png"):
    data = np.load(input_fname)

    plt.plot(data[:,0]/60000,data[:,1], linewidth=0.5) # ms
    # plt.plot(data[:,0]/60000,data[:,2], linewidth=0.5) # HR
    # plt.plot(data[:,0]/60000,data[:,3], linewidth=0.5) # HRV (weighted moving average)
    # plt.plot(data[:,0]/60000,data[:,4], linewidth=0.5) # self.SDNN
    # plt.plot(data[:,0]/60000,data[:,5], linewidth=0.5) # self.SDSD
    # plt.plot(data[:,0]/60000,data[:,6], linewidth=0.5) # self.NN50
    # plt.plot(data[:,0]/60000,data[:,7], linewidth=0.5) # self.rMSSD
    plt.ylabel('dinken')
    plt.savefig(output_fname, bbox_inches='tight', dpi=300)

  def handle_ms(self, ms):
    self.ms_10s_window.append(ms)
    while sum(self.ms_10s_window) > 10000: #
      self.ms_10s_window.pop(0)

      deltas_10s = np.array(list(map(lambda x, y: abs(x-y), self.ms_10s_window[1:], self.ms_10s_window[:-1])))
      self.current_hrv = np.average(deltas_10s, weights=range(len(self.ms_10s_window)-1))

    # self.ms_60s_window.append(ms)
    # while sum(self.ms_60s_window) > 60000: #
    #   self.ms_60s_window.pop(0)

    self.ms_120s_window.append(ms)
    while sum(self.ms_120s_window) > 120000: #
      self.ms_120s_window.pop(0)

      deltas_120s = np.array(list(map(lambda x, y: abs(x-y), self.ms_120s_window[1:], self.ms_120s_window[:-1])))

      #60000 ms in 1 minute
      self.current_hr = 60000 / np.average(self.ms_120s_window, weights=range(len(self.ms_120s_window)))


      # max_hr is een momentopname
      if self.current_hr > self.max_hr:
        self.max_hr = self.current_hr

      # resting hr can be measured over a longer period of time
      if self.current_hr < self.resting_hr:
        self.resting_hr = self.current_hr

      self.sdnn = np.std(self.ms_120s_window)
      self.sdsd = np.std(deltas_120s)
      self.nn50 = np.count_nonzero(deltas_120s >= 50)
      self.rmssd = math.sqrt(np.average(np.square(deltas_120s)))

    # self.ms_300s_window.append(ms)
    # while sum(self.ms_300s_window) > 300000: #
    #   self.ms_300s_window.pop(0)

    return [self.total_ms, ms, self.current_hr, self.current_hrv, self.sdnn, self.sdsd, self.nn50, self.rmssd]


  def read_raw(self):
    A = np.empty((0,8), dtype=float)

    with open('raw/squat_warmup.txt', 'r') as file:
      self.prev_ms = int(file.readline())

      for l in file:
        ms = int(l)
        self.total_ms += ms
        ms_diff = abs(self.prev_ms - ms)

        # if ms_diff <= 100 or ms_diff <= self.current_hrv * 2:
        if True:
          print(f"{self.prev_ms - ms}, {self.current_hrv}")
          newrow = self.handle_ms(ms)

          A = np.append(A, [newrow], axis=0)
        else:
          print(f">>>>>>>> {self.prev_ms - ms}")

        self.prev_ms = ms

    user = [self.resting_hr, self.max_hr]

    print(user)
    #print(A)
    np.save('data.npy', A)


if __name__ == "__main__":
  reader = Datareader()
  reader.read_raw()