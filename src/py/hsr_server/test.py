class BioIndividual:
  NA = 0
  MALE = 1
  FEMALE = 2

  @property
  def museum_object(self):
    return self._museum_object

  @museum_object.setter
  def museum_object(self, value):
    self._museum_object = str(value)

  @property
  def min_age(self):
    return self._min_age

  @min_age.setter
  def min_age(self, value):
    self._min_age = float(value)

  @property
  def max_age(self):
    return self._max_age

  @max_age.setter
  def max_age(self, val):
    self._age = float(max_age)

  @property
  def sex(self):
    return self._sex

  @sex.setter
  def sex(self, val):
    unknown = set(["Unknown", "unknown", "NA", "N/A", "na", "n/a",
      self.NA])
    male = set(["Male", "M", "m", "male", self.MALE])
    female = set(["Female", "F", "f", "female", self.FEMALE])
    if val in unknown:
      self._sex = self.NA
    elif val in male:
      self._sex = self.MALE
    elif val in female:
      self._sez = self.FEMALE

  def __init__(self, indiv_id = None, suffix = None, suffix_design =
      None, min_age = None, max_age = None, sex = None, museum_object = None):
    self.indiv_id = indiv_id
    self.suffix_design = suffix_design
    self.suffix = suffix
    self.min_age = min_age
    self.max_age = max_age
    self.sex = sex
    try:
      self.museum_object = str(museum_object.catalogue_num)
    except AttributeError:
      self.museum_object = str(museum_object)

  def copy(self):
    return BioIndividual(self.indiv_id, self.suffix,
        self.suffix_design, self.min_age,
        self.max_age, self.sex, self.museum_object)

  def __eq__(self, other):
    r = (self.indiv_id == other.indiv_id)
    r = r and (self.suffix_design == other.suffix_design)
    r = r and (self.suffix == other.suffix)
    r = r and (self.min_age == other.min_age)
    r = r and (self.max_age == other.max_age)
    r = r and (self.sex == other.sex)
    r = r and (str(self.museum_object) == str(other.museum_object))
    return r

  def __ne__(self, other):
    return not (self == other)

  def __hash__(self):
    return hash((self.indiv_id, self.suffix, self.suffix_design, self.min_age,
      self.max_age, self.sex, self.museum_object))


class TestDB:
  def test_WriteIndividual(self, db):
    suffix = "a"
    suffix_design = "b"
    min_age = 10
    max_age = 20
    sex = BioIndividual.NA
    nbi = db.newIndividual(suffix, suffix_design, min_age, max_age, sex)
    nbi.min_age += 5
    nbi.suffix_design = "d"
    assert db.writeIndividual(nbi)
    bi = db.getIndividualById(nbi.indiv_id)
    assert nbi == bi


class HSRDBTestImpl():
  def __init__(self):
    self.indivs = set([])
    self.indivs_id = 0

  def newIndividual(self, suffix, suffix_design, min_age, max_age, sex):
    bi = BioIndividual(
        self.indivs_id,
        suffix,
        suffix_design,
        min_age,
        max_age,
        sex)
    self.indivs_id += 1
    self.indivs.add(bi)
    return bi

  def getIndividualById(self, indiv_id):
    for bi in self.indivs:
      if bi.indiv_id == indiv_id:
        return bi.copy()
    return None

  def writeIndividual(self, indiv):
    for bi in self.indivs:
      if bi.indiv_id == indiv.indiv_id:
        self.indivs.remove(bi)
        self.indivs.add(indiv)
        return True
    return None

db = HSRDBTestImpl()
test = TestDB()
test.test_WriteIndividual(db)
