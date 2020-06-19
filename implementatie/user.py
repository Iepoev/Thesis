import h5py

class User:
  """A simple example class"""
  baeke_work = 0
  baeke_sport = 0
  baeke_leisure = 0

  def __init__(self, baeke_work, baeke_sport, baeke_leisure):
    self.baeke_work = baeke_work
    self.baeke_sport = baeke_sport
    self.baeke_leisure = baeke_leisure

  @classmethod
  def fromfile(cls, fname='userdata.hdf5'):
    dset = h5py.File(fname, 'r')['model']
    return cls(dset.attrs['baeke_work'], dset.attrs['baeke_leisure'], dset.attrs['baeke_sport'])

  def __str__(self):
    return 'User(baeke_work={0}, baeke_sport={1}, baeke_leisure={2})'.format(self.baeke_work,self.baeke_sport,self.baeke_leisure)

  def export_hdf5(self, fname = 'userdata.hdf5'):
    f = h5py.File(fname, 'w')
    dset = f.create_dataset("model", (100,), dtype='i')
    dset.attrs['baeke_work'] = self.baeke_work
    dset.attrs['baeke_leisure'] = self.baeke_leisure
    dset.attrs['baeke_sport'] = self.baeke_sport

  def determine_heartrates():
    with io.open('stream', mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
      for line in f:
        print(line.encode('hex'))  # Don't mess up my terminal