
import string

from user import User

def main():
  (work_index,sport_index,leisure_index) = baecke()

  u = User(work_index,sport_index,leisure_index)

  print(u)

def baecke():

  work_index = determine_work_index()

  print('Do you play sports?\n  a: yes\n  b: no\n')
  user_input = input()

  if user_input == "a":
    sport_score = determine_simple_sport_score()
  else:
    sport_score = 0

  sport_index = determine_sport_index(sport_score)
  leisure_index = determine_leisure_index()

  return(work_index,sport_index,leisure_index)

def determine_work_index():
  work_index_questionnaire = [
    ('What is your main occupation?',
    ['a: low activity (driving, desk work, studying, etc.)', 'b: moderate activity (factory work, plumbing, farming, etc.)', 'c: high activity (construction work, dock work, professional sport, etc.)'],
    {"a": 1, "b": 3, "c": 5}),

    ('During my occupation I sit?',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: always'],
    {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1}),

    ('During my occupation I stand?',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: always'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('During my occupation I walk?',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: always'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('During my occupation I lift heavy loads?',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: always'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('After my occupation I am tired?',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('During my occupation I sweat?',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('In comparison of others of my own age I think my occupation is physically ?',
    ['a: much lighter', 'b: lighter', 'c: as heavy', 'd: heavier', 'e: much heavier'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),
  ]

  score = 0

  for q, a, scores in work_index_questionnaire:
    print('{0}\n  {1}\n'.format(q, '\n  '.join(a)))
    user_input = input()

    score += scores[user_input]

  return score / 8


def determine_simple_sport_score():
  sport_score_questionnaire = [
    ('What sport do you play most frequently?',
    ['a: low intensity (biliards, golf, sailing, etc.)', 'b: medium intensity (badminton, cycling, tennis, etc.)', 'c: high intensity (boxing, weightlifting, soccer, etc.)'],
    {"a": 0.76, "b": 1.26, "c": 1.76}),

    ('How many hours do you play a week? ',
    ['a: <1 hour', 'b: 1-2 hours', 'c: 2-3 hours', 'd: 3-4 hours', 'e: >4 hours'],
    {"a": 0.5, "b": 1.5, "c": 2.5, "d": 3.5, "e": 4.5}),

    ('How many months do you play in a year',
    ['a: <1 month', 'b: 1-3 months', 'c: 4-6 months', 'd: 7-9 months', 'e: >9 months'],
    {"a": 0.04, "b": 0.17, "c": 0.42, "d": 0.67, "e": 0.92}),

    ('What sport do you play second most frequently?',
    ['a: low intensity (biliards, golf, sailing, etc.)', 'b: medium intensity (badminton, cycling, tennis, etc.)', 'c: high intensity (boxing, weightlifting, soccer, etc.)'],
    {"a": 0.76, "b": 1.26, "c": 1.76}),

    ('How many hours do you play a week? ',
    ['a: <1 hour', 'b: 1-2 hours', 'c: 2-3 hours', 'd: 3-4 hours', 'e: >4 hours'],
    {"a": 0.5, "b": 1.5, "c": 2.5, "d": 3.5, "e": 4.5}),

    ('How many months do you play in a year',
    ['a: <1 month', 'b: 1-3 months', 'c: 4-6 months', 'd: 7-9 months', 'e: >9 months'],
    {"a": 0.04, "b": 0.17, "c": 0.42, "d": 0.67, "e": 0.92}),
  ]

  score = 1

  for q, a, scores in sport_score_questionnaire:
    print('{0}\n  {1}\n'.format(q, '\n  '.join(a)))
    user_input = input()

    score *= scores[user_input]

  if score >= 12:
    return 5
  elif score >= 8:
    return 4
  elif score >= 4:
    return 3
  elif score >= 0.01:
    return 2
  else:
    return 1


def determine_sport_index(sport_score):
  
  sport_index_questionnaire = [
    ('In comparison with others of my own age I think my physical activity during leisure time is?',
    ['a: much less', 'b: less', 'c: the same', 'd: more', 'e: much more'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('During leisure I sweat',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('During leisure time I play sport',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),
  ]

  score = sport_score

  for q, a, scores in sport_index_questionnaire:
    print('{0}\n  {1}\n'.format(q, '\n  '.join(a)))
    user_input = input()

    score += scores[user_input]

  return score / 4



def determine_leisure_index():
  
  leisure_index_questionnaire = [
    ('During leisure time I watch television',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 5, "b": 3, "c": 3, "d": 2, "e": 1}),

    ('During leisure time I walk',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('During leisure time I cycle',
    ['a: never', 'b: seldom', 'c: sometimes', 'd: often', 'e: very often'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),

    ('How many minutes do you walk and/or cycle per day to and from work school and shopping?',
    ['a: <5 minutes', 'b: 5-15 minutes', 'c: 15-30 minutes', 'd: 30-45 minutes', 'e: >45 minutes'],
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}),
  ]

  score = 0

  for q, a, scores in leisure_index_questionnaire:
    print('{0}\n  {1}\n'.format(q, '\n  '.join(a)))
    user_input = input()

    score += scores[user_input]

  return score / 4


if __name__ == "__main__":
  main()

