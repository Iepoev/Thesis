
import argparse

from user import User
from baecke import baecke

def main():
  parser = argparse.ArgumentParser(description='Fitness coach.')

  parser.add_argument('-f','--file', help='import user data and model from a file')
  parser.add_argument('-i','--init', choices=['full', 'unfit', 'fit'], help='initialize user data, either from scratch or a basic fit/unfit user)')



  args = parser.parse_args()
  print(args)

  (work_index,sport_index,leisure_index) = baecke()

  u = User(work_index,sport_index,leisure_index)

  print(u)


if __name__ == "__main__":
  main()

