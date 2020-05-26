class User:
  """A simple example class"""
  baeke_work = 0
  baeke_sport = 0
  baeke_leisure = 0

  def __init__(self, baeke_work, baeke_sport, baeke_leisure):
    self.baeke_work = baeke_work
    self.baeke_sport = baeke_sport
    self.baeke_leisure = baeke_leisure

  def __str__(self):
    return 'User(baeke_work={0}, baeke_sport={1}, baeke_leisure={2})'.format(self.baeke_work,self.baeke_sport,self.baeke_leisure)
