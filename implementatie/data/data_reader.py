from functools import reduce
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

ACCEPTABLE_RANGE = 0.1

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

  def draw(self, input_fname="data.npy", output_fname="graph.png"):
    data = np.load(input_fname)
    self.draw(data, output_fname)

  def draw(self, data, output_fname="graph.png"):
    plt.plot(data[:,0]/60000,data[:,1], linewidth=0.5) # ms
    # plt.plot(data[:,0]/60000,data[:,2], linewidth=0.5) # HR
    # plt.plot(data[:,0]/60000,data[:,3], linewidth=0.5) # HRV (weighted moving average)
    # plt.plot(data[:,0]/60000,data[:,4], linewidth=0.5) # self.SDNN
    # plt.plot(data[:,0]/60000,data[:,5], linewidth=0.5) # self.SDSD
    # plt.plot(data[:,0]/60000,data[:,6], linewidth=0.5) # self.NN50
    # plt.plot(data[:,0]/60000,data[:,7], linewidth=0.5) # self.rMSSD
    plt.ylabel('dinken')
    plt.ylim((0,1000))
    plt.savefig(output_fname, bbox_inches='tight', dpi=300)

  def handle_ms(self, ms):
    self.ms_10s_window.append(ms)
    while sum(self.ms_10s_window) > 10000: #
      self.ms_10s_window.pop(0)

      deltas_10s = np.array(list(map(lambda x, y: abs(x-y), self.ms_10s_window[1:], self.ms_10s_window[:-1])))
      self.current_hrv = np.average(deltas_10s, weights=range(len(self.ms_10s_window)-1))

      if sum(self.ms_120s_window) < 120000:
        self.current_hr = 60000 / np.average(self.ms_10s_window, weights=range(len(self.ms_10s_window)))

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


  def read_raw(self, fname='raw/2020-06-30 18-00-07 - felix.txt'):
    A = np.empty((0,8), dtype=float)

    with open(fname, 'r') as file:

      queue = []
      ms_7beat_window = []
      is_missing = False

      for l in file:
        new_ms = int(l)
        ms_7beat_window.append(new_ms)


        # 7 beat window:
        # - always append new interval reading (index 6)
        # - check if the interval at index 3 is valid
        # - if something is wrong, try to correct
        # - handle the earliest interval in the queue (index 0)

        # things that can go wrong:
        # - sudden HRV change; the following intervals are in the same range
        #   -> do nothing
        # - previous or following interval averages to correct range
        #   -> one incorrectly measured beat
        #   -> average out both beats
        # - interval is double of the expected range
        #   -> missed a beat
        #   -> halve the interval

        while len(ms_7beat_window) >= 7:
          print(f"{ms_7beat_window}, hrv:{self.current_hrv}")

          ms_diff = abs(ms_7beat_window[2]-ms_7beat_window[3])

          if ms_diff >= 30 or (self.current_hrv >=10 and ms_diff >= self.current_hrv * 2):
            ms_7beat_window = self.find_correction(ms_7beat_window)

          ms = ms_7beat_window.pop(0)

          self.total_ms += ms
          newrow = self.handle_ms(ms)
          A = np.append(A, [newrow], axis=0)

    user = [self.resting_hr, self.max_hr]

    print(user)
    np.save('data.npy', A)
    return A

  def find_correction(self, ms_7beat_window):
    target = (ms_7beat_window[0] + ms_7beat_window[6]) / 2 

    checking_ms = ms_7beat_window[3]

    sudden_change_score = abs(np.average(ms_7beat_window[4:], weights=list(reversed(range(1,len(ms_7beat_window[4:])+1)))) - checking_ms)

    if sudden_change_score < 50:
      return ms_7beat_window
    else:
      missed_beat = ms_7beat_window[:3] + [checking_ms/2, checking_ms/2] + ms_7beat_window[4:]
      missed_beat_score = abs(np.average(ms_7beat_window[:3]+ms_7beat_window[4:])-(checking_ms/2))

      doube_missed_beat = ms_7beat_window[:3] + [checking_ms/3, checking_ms/3, checking_ms/3] + ms_7beat_window[4:]
      doube_missed_beat_score = abs(np.average(ms_7beat_window[:3]+ms_7beat_window[4:])-(checking_ms/3))

      incorrect_beat_ms = (ms_7beat_window[2] + checking_ms) / 2
      incorrect_beat = ms_7beat_window[:2] + [incorrect_beat_ms, incorrect_beat_ms] + ms_7beat_window[4:]
      incorrect_beat_score = abs(np.average(ms_7beat_window[:2]+ms_7beat_window[4:])-incorrect_beat_ms)

      incorrect_with_missed_beat_ms = (ms_7beat_window[2] + checking_ms) / 3
      incorrect_with_missed_beat = ms_7beat_window[:2] + [incorrect_with_missed_beat_ms, incorrect_with_missed_beat_ms, incorrect_with_missed_beat_ms] + ms_7beat_window[4:] 
      incorrect_with_missed_beat_score = abs(np.average(ms_7beat_window[:2]+ms_7beat_window[4:])-incorrect_with_missed_beat_ms)

      windows = [missed_beat, doube_missed_beat, incorrect_beat, incorrect_with_missed_beat]
      ranking = [missed_beat_score, doube_missed_beat_score, incorrect_beat_score, incorrect_with_missed_beat_score]
      lowest = min(ranking)
      if lowest < sudden_change_score:
        return windows[ranking.index(lowest)]
      else:
        print(f"ms_7beat_window {ms_7beat_window}, sudden_change: {sudden_change_score}, missed_beat: {missed_beat_score}, doube_missed_beat: {doube_missed_beat_score}, incorrect_beat: {incorrect_beat_score}, incorrect_with_missed_beat: {incorrect_with_missed_beat_score}")
        return ms_7beat_window

if __name__ == "__main__":
  reader = Datareader()
  # data = reader.read_raw("/raw/2020-07-01 11-06-32 - arnhoudt")
  data = reader.read_raw()
  reader.draw(data, output_fname="graph.png")

