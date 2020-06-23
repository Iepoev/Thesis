
window = []

resting_hr = 220
max_hr = 0

with open('squat_warmup.txt', 'r') as data:
  ms = line = fp.readline()

  list_data = string_data.split(',')
  list_data.pop()
  data_array = np.array(list_data, dtype=float).reshape(10000, 1000)

np.save('data.npy', data_array)