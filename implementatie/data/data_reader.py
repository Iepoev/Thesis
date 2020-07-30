from functools import reduce
import numpy as np
import math
import operator
import matplotlib.pyplot as plt

import scipy.signal
import scipy
import warnings

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

    # 2 minutes rest
    # 5 minutes almost not active
    # 5 minutes active
    # 2 minute recovering
    # 5 minute active
    # 2 minute recovering
    # 5 minute intense
    # 1 minute maximal exertion
    # 3 minutes recovery
    self.exercise_markers_ms = [120000,420000,720000,840000,1140000,1260000,1560000,1620000,1860000]

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

    self.current_max = 0
    self.current_min = 0
    self.current_hrr = 0

  def save_to_npy(self, data, fname="data.npy"):
    np.save(fname, data)

  def draw(self, input_fname="data.npy", output_fname="graph.png"):
    data = np.load(input_fname)
    self.draw(data, output_fname)

  def draw(self, data, output_fname="graph.png"):
    plt.plot(data[:,0]/60000,data[:,1], linewidth=0.2) # ms
    plt.plot(data[:,0]/60000,data[:,2], linewidth=0.2) # HR
    plt.plot(data[:,0]/60000,data[:,3], linewidth=0.2) # HRV (weighted moving average)
    # plt.plot(data[:,0]/60000,data[:,4], linewidth=0.2) # SDNN
    # plt.plot(data[:,0]/60000,data[:,5], linewidth=0.2) # SDSD
    # plt.plot(data[:,0]/60000,data[:,6], linewidth=0.2) # NN50
    # plt.plot(data[:,0]/60000,data[:,7], linewidth=0.2) # rMSSD
    # plt.plot(data[:,0]/60000,data[:,8], linewidth=0.2) # 60s VLF
    # plt.plot(data[:,0]/60000,data[:,9], linewidth=0.2) # 60s LF
    # plt.plot(data[:,0]/60000,data[:,10], linewidth=0.2) # 60s HF
    # plt.plot(data[:,0]/60000,data[:,11], linewidth=0.2) # 60s LF/HF
    # plt.plot(data[:,0]/60000,data[:,12], linewidth=0.2) # 300s VLF
    # plt.plot(data[:,0]/60000,data[:,13], linewidth=0.2) # 300s LF
    # plt.semilogy(data[:,0]/60000,data[:,14], linewidth=0.2) # 300s HF
    # plt.plot(data[:,0]/60000,data[:,15], linewidth=0.2) # 300s LF/HF
    # plt.plot(data[:,0]/60000,data[:,-1], linewidth=0.2) # category

    for i in self.exercise_markers_ms:
      plt.axvline(x=i/60000, linewidth=0.1)

    plt.ylabel('dinken')
    # plt.ylim((0,1000))
    plt.savefig(output_fname, bbox_inches='tight', dpi=800)

  def handle_ms(self, ms):

    self.ms_10s_window.append(ms)
    while sum(self.ms_10s_window) > 10000: #
      self.ms_10s_window.pop(0)

      deltas_10s = np.array(list(map(lambda x, y: abs(x-y), self.ms_10s_window[1:], self.ms_10s_window[:-1])))
      self.current_hrv = np.average(deltas_10s, weights=range(len(self.ms_10s_window)-1))

    self.ms_60s_window.append(ms)
    while sum(self.ms_60s_window) > 60000: #
      self.ms_60s_window.pop(0)

      (self.vlf_power_60s, self.lf_power_60s, self.hf_power_60s, self.lf_hf_ratio_60s) = self.handle_powerband(self.ms_60s_window)

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
      (self.vlf_power_300s, self.lf_power_300s, self.hf_power_300s, self.lf_hf_ratio_300s) = self.handle_powerband(self.ms_300s_window)


    if len(self.ms_120s_window) > 1:
      self.current_hr = 60000 / np.average(self.ms_120s_window, weights=range(len(self.ms_120s_window)))

    # categories:
    # 0: resting
    # 1: active
    # 2: recovering

    if self.total_ms < self.exercise_markers_ms[0]:
      cur_cat = 0 # 2 minutes rest
    elif self.total_ms < self.exercise_markers_ms[1]:
      cur_cat = 0 # 5 minutes almost not active
    elif self.total_ms < self.exercise_markers_ms[2]:
      cur_cat = 1 # 5 minutes active
    elif self.total_ms < self.exercise_markers_ms[3]:
      cur_cat = 2 # 2 minute recovering
    elif self.total_ms < self.exercise_markers_ms[4]:
      cur_cat = 1 # 5 minute active
    elif self.total_ms < self.exercise_markers_ms[5]:
      cur_cat = 2 # 2 minute recovering
    elif self.total_ms < self.exercise_markers_ms[6]:
      cur_cat = 1 # 5 minute intense
    elif self.total_ms < self.exercise_markers_ms[7]:
      cur_cat = 1 # 1 minute maximal exertion
    elif self.total_ms < self.exercise_markers_ms[8]:
      cur_cat = 2 # 3 minutes recovery
    else:
      cur_cat = 2

    return [
      self.total_ms, 
      ms, 
      self.current_hr,
      self.current_hrv,
      self.sdnn,
      self.sdsd,
      self.nn50,
      self.rmssd,
      # self.vlf_power_60s,
      # self.lf_power_60s,
      self.hf_power_60s,
      # self.lf_hf_ratio_60s,
      self.vlf_power_300s, 
      self.lf_power_300s, 
      # self.hf_power_300s, 
      self.lf_hf_ratio_300s,
      cur_cat
    ]

  def handle_powerband(self, window):
      # sample all signals up to (0.8/2 = 4) Hz
      # nperseg is chosen as a common multiplier of the frequency bands
      f, Pxx_den = scipy.signal.welch(window, 0.8, nperseg=5280)

      # sometimes welch has not enough inputs and changes the nperseg to fit
      # so create the frequency bands dynamically
      n_segs = len(Pxx_den)
      vlf_lower_lim = math.floor((0.0033/0.4)*n_segs) # 0.0033 Hz is the lower limit of the VLF band
      vlf_upper_lim = math.floor((0.04/0.4)*n_segs) # 0.04 Hz is the upper limit of the VLF band
      lf_upper_lim = math.floor((0.15/0.4)*n_segs) # 0.04 Hz is the upper limit of the LF band

      vlf_power = sum(Pxx_den[vlf_lower_lim:vlf_upper_lim])
      lf_power = sum(Pxx_den[vlf_upper_lim:lf_upper_lim])
      hf_power = sum(Pxx_den[lf_upper_lim:-1])
      lf_hf_ratio = lf_power/hf_power if hf_power > 0 else 0

      return (vlf_power, lf_power, hf_power, lf_hf_ratio)



  def read_raw(self, fname, oname="data", correct=True, userdata=True, userprofile=True):
    data = np.empty((0,13), dtype=float)

    with open(fname, 'r') as file:

      queue = []
      ms_7beat_window = []
      is_missing = False

      for l in file:
        new_ms = int(l)
        ms_7beat_window.append(new_ms)

        while len(ms_7beat_window) >= 7 and self.total_ms < self.exercise_markers_ms[8]:
          # print(f"{ms_7beat_window}, hrv:{self.current_hrv}")

          ms_diff = abs(ms_7beat_window[2]-ms_7beat_window[3])

          if correct and (ms_diff >= 50 or (self.current_hrv >=10 and ms_diff >= self.current_hrv * 3)):
            ms_7beat_window = self.find_correction(ms_7beat_window)

          ms = ms_7beat_window.pop(0)

          self.total_ms += ms
          newrow = self.handle_ms(ms)
          data = np.append(data, [newrow], axis=0)

    if userdata:
      self.handle_user_data(data, oname)

    if userprofile:
      self.handle_user_profile(data, oname)

    np.save(f'processed/{oname}.npy', data[1:])
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

    # take the weighted average of all future beats and see how it compares to our beat that we are correcting
    sudden_change_score = abs(np.average(ms_7beat_window[4:], weights=list(reversed(range(1,len(ms_7beat_window[4:])+1)))) - checking_ms)


    # for each proposed solution, calculate a score:
    # it takes the difference between the average of "correct" beats and 
    # the proposed corrected beat, if it is close it means that this correction
    # is valid
    if sudden_change_score < 50:
      return ms_7beat_window
    else:
      missed_beat = ms_7beat_window[:3] + [checking_ms/2, checking_ms/2] + ms_7beat_window[4:]
      missed_beat_score = abs(np.average(ms_7beat_window[:3]+ms_7beat_window[4:])-(checking_ms/2))

      doube_missed_beat = ms_7beat_window[:3] + [checking_ms/3, checking_ms/3, checking_ms/3] + ms_7beat_window[4:]
      doube_missed_beat_score = abs(np.average(ms_7beat_window[:3]+ms_7beat_window[4:])-(checking_ms/3))

      incorrect_beat_ms = (ms_7beat_window[2] + checking_ms + ms_7beat_window[4]) / 3
      incorrect_beat = ms_7beat_window[:2] + [incorrect_beat_ms, incorrect_beat_ms, incorrect_beat_ms] + ms_7beat_window[5:]
      incorrect_beat_score = abs(np.average(ms_7beat_window[:2]+ms_7beat_window[4:])-incorrect_beat_ms)

      incorrect_with_missed_beat_ms = (ms_7beat_window[2] + checking_ms) / 3
      incorrect_with_missed_beat = ms_7beat_window[:2] + [incorrect_with_missed_beat_ms, incorrect_with_missed_beat_ms, incorrect_with_missed_beat_ms] + ms_7beat_window[4:] 
      incorrect_with_missed_beat_score = abs(np.average(ms_7beat_window[:2]+ms_7beat_window[4:])-incorrect_with_missed_beat_ms)

      text = ["missed_beat", "doube_missed_beat", "incorrect_beat", "incorrect_with_missed_beat"]

      windows = [missed_beat, doube_missed_beat, incorrect_beat, incorrect_with_missed_beat]
      ranking = [missed_beat_score, doube_missed_beat_score, incorrect_beat_score, incorrect_with_missed_beat_score]
      lowest = min(ranking)
      if lowest < sudden_change_score:
        print(f"ms_7beat_window {ms_7beat_window} handled using {text[ranking.index(lowest)]} with score {lowest} to {windows[ranking.index(lowest)]}")

        return windows[ranking.index(lowest)]
      else:
        print(f"unhandled! ms_7beat_window {ms_7beat_window}, sudden_change: {sudden_change_score}, missed_beat: {missed_beat_score}, doube_missed_beat: {doube_missed_beat_score}, incorrect_beat: {incorrect_beat_score}, incorrect_with_missed_beat: {incorrect_with_missed_beat_score}")
        return ms_7beat_window

  def handle_exertion_window(self, data):
    print(f"exertion {data[0,0]}, {data.shape}")

    # powerbands
    (vlf_power, lf_power, hf_power, lf_hf_ratio) = self.handle_powerband(data[:,1])

    max_hr = np.max(data[:,2])

    deltas = np.array(list(map(lambda x, y: abs(x-y), data[1:,1], data[:-1,1])))
    rMSSD = math.sqrt(np.average(np.square(deltas)))

    return (vlf_power, lf_power, hf_power, lf_hf_ratio, max_hr, rMSSD)


  def handle_recovery_window(self, data):
    print(f"recovery {data[0,0]}, {data.shape}")

    # powerbands
    (vlf_power, lf_power, hf_power, lf_hf_ratio) = self.handle_powerband(data[:,1])

    hr_max = np.max(data[:,2])
    hr_max_ts = data[np.argmax(data[:,2]),0]
    hr_min = np.min(data[:,2])
    hrr_1min = hr_max - data[np.argmax(data[0]>(hr_max_ts+60000)),2]

    hrr_2min = 0
    if (np.argmax(data[0]>(data[0,0]+120000))):
      hrr_2min = hr_max - data[np.argmax(data[0]>(hr_max_ts+120000)),2]
    else:
      hrr_2min = hr_max - data[-1,2]

    deltas = np.array(list(map(lambda x, y: abs(x-y), data[1:,1], data[:-1,1])))
    rMSSD = math.sqrt(np.average(np.square(deltas)))

    return (vlf_power, lf_power, hf_power, lf_hf_ratio, hr_max, hrr_1min, hrr_2min, rMSSD)


  def handle_user_data(self, data, oname):

    (total_vlf_power, total_lf_power, total_hf_power, total_lf_hf_ratio) = self.handle_powerband(data[:,1])
    (ex1_vlf, ex1_lf, ex1_hf, ex1_lf_hf, ex1_max_hr, ex1_rMSSD) = self.handle_exertion_window(data[(data[:,0] > self.exercise_markers_ms[0]) & (data[:,0] < self.exercise_markers_ms[1])])
    (ex2_vlf, ex2_lf, ex2_hf, ex2_lf_hf, ex2_max_hr, ex2_rMSSD) = self.handle_exertion_window(data[(data[:,0] > self.exercise_markers_ms[1]) & (data[:,0] < self.exercise_markers_ms[2])])
    (rec1_vlf, rec1_lf, rec1_hf, rec1_lf_hf, rec1_hr_max, rec1_hrr_1min, rec1_hrr_end, rec1_rMSSD) = self.handle_recovery_window(data[(data[:,0] > self.exercise_markers_ms[2]) & (data[:,0] < self.exercise_markers_ms[3])])
    (ex3_vlf, ex3_lf, ex3_hf, ex3_lf_hf, ex3_max_hr, ex3_rMSSD) = self.handle_exertion_window(data[(data[:,0] > self.exercise_markers_ms[3]) & (data[:,0] < self.exercise_markers_ms[4])])
    (rec2_vlf, rec2_lf, rec2_hf, rec2_lf_hf, rec2_hr_max, rec2_hrr_1min, rec2_hrr_end, rec2_rMSSD) = self.handle_recovery_window(data[(data[:,0] > self.exercise_markers_ms[4]) & (data[:,0] < self.exercise_markers_ms[5])])
    (ex4_vlf, ex4_lf, ex4_hf, ex4_lf_hf, ex4_max_hr, ex4_rMSSD) = self.handle_exertion_window(data[(data[:,0] > self.exercise_markers_ms[5]) & (data[:,0] < self.exercise_markers_ms[6])])
    (ex5_vlf, ex5_lf, ex5_hf, ex5_lf_hf, ex5_max_hr, ex5_rMSSD) = self.handle_exertion_window(data[(data[:,0] > self.exercise_markers_ms[6]) & (data[:,0] < self.exercise_markers_ms[7])])
    (rec3_vlf, rec3_lf, rec3_hf, rec3_lf_hf, rec3_hr_max, rec3_hrr_1min, rec3_hrr_end, rec3_rMSSD) = self.handle_recovery_window(data[(data[:,0] > self.exercise_markers_ms[7]) & (data[:,0] < self.exercise_markers_ms[8])])


    user_data = [
      self.resting_hr, 
      self.max_hr, 
      total_vlf_power, 
      total_lf_power, 
      total_hf_power, 
      total_lf_hf_ratio,

      ex1_vlf, 
      ex1_lf, 
      ex1_hf, 
      ex1_lf_hf, 
      ex1_max_hr, 
      ex1_rMSSD,

      ex2_vlf, 
      ex2_lf, 
      ex2_hf, 
      ex2_lf_hf, 
      ex2_max_hr, 
      ex2_rMSSD,

      rec1_vlf, 
      rec1_lf, 
      rec1_hf, 
      rec1_lf_hf, 
      rec1_hr_max, 
      rec1_hrr_1min, 
      rec1_hrr_end, 
      rec1_rMSSD,

      ex3_vlf, 
      ex3_lf, 
      ex3_hf, 
      ex3_lf_hf, 
      ex3_max_hr, 
      ex3_rMSSD,

      rec2_vlf, 
      rec2_lf, 
      rec2_hf, 
      rec2_lf_hf, 
      rec2_hr_max, 
      rec2_hrr_1min, 
      rec2_hrr_end, 
      rec2_rMSSD,

      ex4_vlf, 
      ex4_lf, 
      ex4_hf, 
      ex4_lf_hf, 
      ex4_max_hr, 
      ex4_rMSSD,

      ex5_vlf, 
      ex5_lf, 
      ex5_hf, 
      ex5_lf_hf, 
      ex5_max_hr, 
      ex5_rMSSD,

      rec3_vlf, 
      rec3_lf, 
      rec3_hf, 
      rec3_lf_hf, 
      rec3_hr_max, 
      rec3_hrr_1min, 
      rec3_hrr_end, 
      rec3_rMSSD,
    ]

    np.save(f'processed/{oname}_data.npy', user_data)


  def handle_user_profile(self, data, oname):

    ####################
    # SET 1 50W 50 RPM #
    ####################

    print('enter user RPE for set 1 (50W 50 RPM)')
    rpe_1 = input()

    #####################
    # SET 2 100W 50 RPM #
    #####################

    print('enter user RPE for set 2 (100W 50 RPM)')
    rpe_2 = input()

    ################
    # SET 3 60% HR #
    ################

    print('enter user RPE for set 3 (60%)')
    rpe_3 = input()

    print('enter user Kcal for set 3 (60%))')
    kcal_3 = input()

    print('enter user Dist for set 3 (60%))')
    dist_3 = input()


    ################
    # SET 4 80% HR #
    ################

    print('enter user RPE for set 4 (80%)')
    rpe_4 = input()

    print('enter user Kcal for set 4 (80%))')
    kcal_4 = input()

    print('enter user Dist for set 4 (80%))')
    dist_4 = input()

    ################
    # SET 5 60% HR #
    ################

    print('enter user Kcal for set 5 (99%))')
    kcal_5 = input()

    print('enter user Dist for set 5 (99%))')
    dist_5 = input()


    print('enter user Baeke score (W)')
    baeke_W = input()

    print('enter user Baeke score (S)')
    baeke_S = input()

    print('enter user Baeke score (L)')
    baeke_L = input()

    user_profile = [
      int(rpe_2)-int(rpe_1),
      int(rpe_3)-int(rpe_1),
      int(kcal_3),
      int(dist_3),
      int(rpe_4)-int(rpe_1),
      int(kcal_4),
      int(dist_4),
      int(kcal_5)-int(kcal_4),
      int(dist_5)-int(dist_4),
      float(baeke_W),
      float(baeke_S),
      float(baeke_L)
    ]
    np.save(f'processed/{oname}_profile.npy', user_profile)


if __name__ == "__main__":

  scipy.special.seterr(all='ignore')
  warnings.simplefilter("ignore", UserWarning)

  reader = Datareader()

  Datareader().read_raw("raw/2020-06-27 22-08-21 - poef 1.txt", oname="poef_1", userprofile=False)
  Datareader().read_raw("raw/2020-06-28 17-34-47 - poef 2.txt", oname="poef_2", userprofile=False)
  Datareader().read_raw("raw/2020-06-29 14-37-18 - marcon.txt", oname="marcon", userprofile=False)
  Datareader().read_raw("raw/2020-06-29 15-21-44 - wouwt.txt", oname="wouwt", userprofile=False)
  Datareader().read_raw("raw/2020-06-30 18-00-07 - felix.txt", oname="felix", userprofile=False)
  Datareader().read_raw("raw/2020-06-30 18-43-53 - charlotte.txt", oname="charlotte", userprofile=False)
  Datareader().read_raw("raw/2020-06-30 19-27-41 - francis.txt", oname="francis", userprofile=False) # niet goed
  Datareader().read_raw("raw/2020-07-01 11-06-32 - arnhoudt.txt", oname="arnhoudt", userprofile=False) # niet goed
  Datareader().read_raw("raw/2020-07-04 15-23-00 - maxime.txt", oname="maxime", userprofile=False)
  Datareader().read_raw("raw/2020-07-09 11-25-59 - karolina.txt", oname="karolina", userprofile=False)
  Datareader().read_raw("raw/2020-07-14 17-38-27 - jochen.txt", oname="jochen", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 11-19-17 - jessie.txt", oname="jessie", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 14-08-25 - midgard.txt", oname="midgard", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 17-50-10 - Dorre.txt", oname="Dorre", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 18-37-49 - Anton.txt", oname="Anton", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 19-23-42 - Wolf.txt", oname="Wolf", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 20-07-47 - Sander.txt", oname="Sander", userprofile=False)
  Datareader().read_raw("raw/2020-07-24 20-53-05 - Ward.txt", oname="Ward", userprofile=False)
  Datareader().read_raw("raw/2020-07-25 10-53-46 - Blomme.txt", oname="Blomme", userprofile=False)
  Datareader().read_raw("raw/2020-07-26 10-12-10 - Arthur.txt", oname="Arthur", userprofile=False)
  Datareader().read_raw("raw/2020-07-26 16-08-03 - Silke.txt", oname="Silke", userprofile=False)
  Datareader().read_raw("raw/2020-07-27 10-09-45 - Leendert.txt", oname="Leendert", userprofile=False)
  Datareader().read_raw("raw/2020-07-27 10-56-48 - Xeno.txt", oname="Xeno", userprofile=False)
  Datareader().read_raw("raw/2020-07-28 15-22-10 - Lisa.txt", oname="Lisa", userprofile=False)

  # data = Datareader().read_raw("raw/2020-07-02 22-23-08 - poef - interval.txt", oname="poef_interval.npy")
  

  # Datareader().read_raw("raw/squat_3x5.txt")
  # Datareader().read_raw("raw/squat_rest.txt")
  # Datareader().read_raw("raw/squat_warmup.txt")


  # reader = Datareader()
  # data = reader.read_raw("raw/2020-06-29 14-37-18 - marcon.txt", oname="marcon.npy")
  # data = reader.read_raw("raw/2020-07-09 11-25-59 - karolina.txt", oname="karolina.npy")
  # reader.draw(data, output_fname="out.png")

