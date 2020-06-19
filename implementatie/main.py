
import argparse

from user import User
from baecke import baecke

def tensorflow():
  # TensorFlow and tf.keras
  import tensorflow as tf
  from tensorflow import keras

  # Helper libraries
  import numpy as np
  import matplotlib.pyplot as plt

  print(tf.__version__)


def main():
  parser = argparse.ArgumentParser(description='Fitness coach.')

  parser.add_argument('-f','--file', const='userdata.hdf5', nargs='?', help='import user data and model from a file')
  parser.add_argument('-i','--init', default='fromscratch', nargs='?', choices=['fromscratch', 'inactive', 'active', 'elite'], help='initialize user data, either from scratch or a basic fit/unfit user)')

  args = parser.parse_args()
  print(args)

  if args.file:
    u = User.fromfile(fname=args.file)
    print(u)
  else:
    if args.init == 'fromscratch':
      (work_index,sport_index,leisure_index) = baecke()
      u = User(work_index,sport_index,leisure_index)
      print(u)
      u.export_hdf5()
    elif args.init == 'inactive':
      u = User(2.0, 2.0, 1.0)
      print(u)
      u.export_hdf5()
    elif args.init == 'active':
      u = User(2.0, 4.0, 3.0)
      print(u)
      u.export_hdf5()
    elif args.init == 'elite':
      u = User(4.5, 5.0, 4.0)
      print(u)
      u.export_hdf5()

  tensorflow()

if __name__ == "__main__":
  main()

