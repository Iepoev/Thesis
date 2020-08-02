from glob import glob
import os.path
import numpy as np

for data_fname in glob("data/processed/*_data.npy"):
  # Load file
  name = os.path.basename(data_fname[:-9]) # strip "_data.npy" from fname
  data = np.load(data_fname)

  profile_fname = os.path.dirname(data_fname) + "/" + name + "_profile.npy"
  (rpe_2, rpe_3, kcal_3, dist_3, rpe_4, kcal_4, dist_4, kcal_5, dist_5, baeke_W, baeke_S, baeke_L) = np.load(profile_fname)


  user_profile = [
    data[0], # resting hr,
    data[1], # max hr
    data[10], # ex1_max_hr,
    int(rpe_2),
    data[16], # ex2_max_hr,
    int(rpe_3),
    int(kcal_3),
    int(dist_3),
    int(rpe_4),
    int(kcal_4),
    int(dist_4),
    int(kcal_5),
    int(dist_5),
    float(baeke_W),
    float(baeke_S),
    float(baeke_L)
  ]

  np.save(f'data/processed/{name}_profile.npy', user_profile)
