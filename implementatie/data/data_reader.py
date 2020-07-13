from functools import reduce
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

import scipy

# Import packages
import pyhrv
import pyhrv.frequency_domain as fd

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

    self.ms_10s_window = []
    self.ms_60s_window = []
    self.ms_120s_window = []
    self.ms_300s_window = []
    self.total_ms = 0

    # store parameters in class variables for when a new beat
    # doesn't cross a window threshold.
    # In this case the previous values can be used
    self.current_hr = 0
    self.current_hrv = 0
    self.sdnn = 0
    self.sdsd = 0
    self.nn50 = 0
    self.rmssd = 0

    self.vlf_power_60s = 0
    self.lf_power_60s = 0
    self.hf_power_60s = 0
    self.lf_hf_ratio_60s = 0

    self.vlf_power_300s = 0
    self.lf_power_300s = 0
    self.hf_power_300s = 0
    self.lf_hf_ratio_300s = 0

  def save_to_npy(self, data, fname="data.npy"):
    np.save(fname, data)

  def draw(self, input_fname="data.npy", output_fname="graph.png"):
    data = np.load(input_fname)
    self.draw(data, output_fname)

  def draw(self, data, output_fname="graph.png"):
    # plt.plot(data[:,0]/60000,data[:,1], linewidth=0.5) # ms
    plt.plot(data[:,0]/60000,data[:,2], linewidth=0.5) # HR
    plt.plot(data[:,0]/60000,data[:,3], linewidth=0.5) # HRV (weighted moving average)
    # plt.plot(data[:,0]/60000,data[:,4], linewidth=0.5) # SDNN
    # plt.plot(data[:,0]/60000,data[:,5], linewidth=0.5) # SDSD
    # plt.plot(data[:,0]/60000,data[:,6], linewidth=0.5) # NN50
    # plt.plot(data[:,0]/60000,data[:,7], linewidth=0.5) # rMSSD
    # plt.plot(data[:,0]/60000,data[:,8], linewidth=0.5) # 60s VLF
    # plt.plot(data[:,0]/60000,data[:,9], linewidth=0.5) # 60s LF
    # plt.plot(data[:,0]/60000,data[:,10], linewidth=0.5) # 60s HF
    # plt.plot(data[:,0]/60000,data[:,11], linewidth=0.5) # 60s LF/HF
    # plt.plot(data[:,0]/60000,data[:,12], linewidth=0.5) # 300s VLF
    # plt.plot(data[:,0]/60000,data[:,13], linewidth=0.5) # 300s LF
    # plt.semilogy(data[:,0]/60000,data[:,14], linewidth=0.5) # 300s HF
    # plt.plot(data[:,0]/60000,data[:,15], linewidth=0.5) # 300s LF/HF
    plt.plot(data[:,0]/60000,data[:,16], linewidth=0.5) # category
    plt.ylabel('dinken')
    # plt.ylim((0,1000))
    plt.savefig(output_fname, bbox_inches='tight', dpi=300)

  def handle_ms(self, ms):

    self.ms_10s_window.append(ms)
    while sum(self.ms_10s_window) > 10000: #
      self.ms_10s_window.pop(0)

      deltas_10s = np.array(list(map(lambda x, y: abs(x-y), self.ms_10s_window[1:], self.ms_10s_window[:-1])))
      self.current_hrv = np.average(deltas_10s, weights=range(len(self.ms_10s_window)-1))

    self.ms_60s_window.append(ms)
    while sum(self.ms_60s_window) > 60000: #
      self.ms_60s_window.pop(0)

      f, Pxx_den_60s = scipy.signal.welch(self.ms_60s_window, 0.8, nperseg=5280)

      self.vlf_power_60s = sum(Pxx_den_60s[21:253])
      self.lf_power_60s = sum(Pxx_den_60s[253:948])
      self.hf_power_60s = sum(Pxx_den_60s[948:-1])
      self.lf_hf_ratio_60s = self.lf_power_60s/self.hf_power_60s if self.hf_power_60s > 0 else 0

    self.ms_120s_window.append(ms)
    while sum(self.ms_120s_window) > 120000: #
      self.ms_120s_window.pop(0)

      deltas_120s = np.array(list(map(lambda x, y: abs(x-y), self.ms_120s_window[1:], self.ms_120s_window[:-1])))

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

    self.ms_300s_window.append(ms)
    while sum(self.ms_300s_window) > 300000: #
      self.ms_300s_window.pop(0)

      f, Pxx_den_300s = scipy.signal.welch(self.ms_300s_window, 0.8, nperseg=5280)

      self.vlf_power_300s = sum(Pxx_den_300s[21:253])
      self.lf_power_300s = sum(Pxx_den_300s[253:948])
      self.hf_power_300s = sum(Pxx_den_300s[948:-1])
      self.lf_hf_ratio_300s = self.lf_power_300s/self.hf_power_300s if self.hf_power_300s > 0  else 0

    if len(self.ms_120s_window) > 1:
      self.current_hr = 60000 / np.average(self.ms_120s_window, weights=range(len(self.ms_120s_window)))

    # categories:
    # 0: resting
    # 1: moving
    # 2: active
    # 3: intense
    # 4: maximal exertion
    # 5: recovering (fast)
    # 6: recovering (slow)

    if self.total_ms < 120000:
      cur_cat = 0 # 2 minutes rest
    elif self.total_ms < 420000:
      cur_cat = 10 # 10 minutes active
    elif self.total_ms < 720000:
      cur_cat = 20 # 10 minutes active
    elif self.total_ms < 840000:
      cur_cat = 50 # 2 minute recovering
    elif self.total_ms < 1140000:
      cur_cat = 20 # 5 minute rest
    elif self.total_ms < 1260000:
      cur_cat = 50 # 2 minute recovering
    elif self.total_ms < 1560000:
      cur_cat = 30 # 5 minute intense
    elif self.total_ms < 1620000:
      cur_cat = 40 # 1 minute maximal exertion
    else:
      cur_cat = 60

    return [
      self.total_ms, 
      ms, 
      self.current_hr,
      self.current_hrv,
      self.sdnn,
      self.sdsd,
      self.nn50,
      self.rmssd,
      self.vlf_power_60s,
      self.lf_power_60s,
      self.hf_power_60s,
      self.lf_hf_ratio_60s,
      self.vlf_power_300s, 
      self.lf_power_300s, 
      self.hf_power_300s, 
      self.lf_hf_ratio_300s,
      cur_cat,
    ]


  def read_raw(self, fname, oname="data.npy", correct=True):
    data = np.empty((0,17), dtype=float)

    with open(fname, 'r') as file:

      queue = []
      ms_7beat_window = []
      is_missing = False

      for l in file:
        new_ms = int(l)
        ms_7beat_window.append(new_ms)

        while len(ms_7beat_window) >= 7 and self.total_ms < 2400000:
          print(f"{ms_7beat_window}, hrv:{self.current_hrv}")

          ms_diff = abs(ms_7beat_window[2]-ms_7beat_window[3])

          if ms_diff >= 30 or (self.current_hrv >=10 and ms_diff >= self.current_hrv * 2):
            ms_7beat_window = self.find_correction(ms_7beat_window)

          ms = ms_7beat_window.pop(0)

          self.total_ms += ms
          newrow = self.handle_ms(ms)
          data = np.append(data, [newrow], axis=0)



    f, Pxx_den = scipy.signal.welch(data[:,1], 0.8, nperseg=5280)

    user = [self.resting_hr, self.max_hr, sum(Pxx_den[21:253]), sum(Pxx_den[253:948]), sum(Pxx_den[948:-1])]

    print(user)
    np.save(f'processed/{oname}', data)
    return data

  def find_correction(self, ms_7beat_window):

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
  Datareader().read_raw("raw/2020-06-27 22-08-21 - poef 1.txt", oname="poef_1.npy")
  Datareader().read_raw("raw/2020-06-28 17-34-47 - poef 2.txt", oname="poef_2.npy")
  Datareader().read_raw("raw/2020-06-29 14-37-18 - marcon.txt", oname="marcon.npy")
  Datareader().read_raw("raw/2020-06-29 15-21-44 - wouwt.txt", oname="wouwt.npy")
  Datareader().read_raw("raw/2020-06-30 18-00-07 - felix.txt", oname="felix.npy")
  Datareader().read_raw("raw/2020-06-30 18-43-53 - charlotte.txt", oname="charlotte.npy")
  Datareader().read_raw("raw/2020-06-30 19-27-41 - francis.txt", oname="francis.npy")
  Datareader().read_raw("raw/2020-07-01 11-06-32 - arnhoudt.txt", oname="arnhoudt.npy")
  Datareader().read_raw("raw/2020-07-04 15-23-00 - maxime.txt", oname="maxime.npy")
  Datareader().read_raw("raw/2020-07-09 11-25-59 - karolina.txt", oname="karolina.npy")

  # Datareader().read_raw("raw/2020-07-02 22-23-08 - poef - interval.txt", oname="poef_interval.npy")
  
  # Datareader().read_raw("raw/squat_3x5.txt")
  # Datareader().read_raw("raw/squat_rest.txt")
  # Datareader().read_raw("raw/squat_warmup.txt")

  # reader.draw(data, output_fname="graph.png")

