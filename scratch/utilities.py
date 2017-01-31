from collections import defaultdict
import json


class NamesIdDictionary(object):

  def __init__(self, differentiator=lambda x, y: False,
               name_field='names', id_field='id'):
    """differentiator is a function that returns True if x and y is different.
    """
    # To pair ids to their institutions
    self._ids_to_items = {}

    # For when a single institution has different ids
    self._ids_to_ids_dict = {}

    # To pair institution names to their ids
    self._names_to_ids_dict = defaultdict(lambda : set())

    self._different = differentiator

    self._name_fld = name_field
    self._id_fld = id_field

  def get_ids_from_id(self, id):
    return self._ids_to_ids_dict.get(id)

  def get_id_from_name(self, name):
    return self._names_to_ids_dict.get(name)

  def get(self, id):
      return self._ids_to_items.get(id)

  def add(self, item):
    id = item.get(self._id_fld)
    name = item.get(self._name_fld)

    if not id:
        raise KeyError('ID can not be None.')

    if self._ids_to_items.get(id, None):
        # We have an item with the same ID
        # We need to check whether it's the same or not
        if self._different(item, self._ids_to_items[id]):
            print('Two items with equal ids are different: {}, {}'.format(
                    str(item), str(self._ids_to_items[id])))
            return

    self._ids_to_items[id] = item

    if not name:
        # If we don't know the name, then there's nothing to do
        return

    self._names_to_ids_dict[name].add(id)
    known_ids = self._names_to_ids_dict[name]

    for _id in known_ids:
        self._ids_to_ids_dict[_id] = known_ids


def clean_up_dict(d):
  return {k:v for k, v in d.items() if v is not None}

def contains_data(arg):
  if isinstance(arg, dict):
    values = [v for k, v in arg.items()]
  elif isinstance(arg, list):
    values = [v for v in arg]
  else:
    values = [arg]
  return any(values)


class PaperGenerator(object):

  def __init__(self, file_name='data/paperData.json'):
    self._file_name = file_name

  def next_paper(self):
    return next(self._iterator)

  def __iter__(self):
    self.papers = json.load(open(self._file_name, 'r'))
    self._iterator = iter(self.papers)
    return self

  def __next__(self):
    return self.next_paper()

  def next(self):
    return self.next_paper()


class OpenRefinePaperGenerator(PaperGenerator):

  def __init__(self, file_name='data/scopusRefined.json'):
    self._file_name = file_name

  def __iter__(self):
    self.json_list = json.load(open(self._file_name, 'r'))
    self._iterator = iter(self.json_list)
    self._next_paper_base = next(self._iterator)
    return self

  def format_output_paper(self, paper):
    paper['authors'] = [clean_up_dict(author)
                        for author in paper['authors']
                        if contains_data(author)]
    paper['affiliations'] = [clean_up_dict(institution)
                             for institution in paper['affiliations']
                             if contains_data(institution)]
    res = clean_up_dict(paper)
    return res

  def next_paper(self):
    paper_base = self._next_paper_base
    if not paper_base:
      raise StopIteration
    if not paper_base.get('pubName'):
      raise ValueError('The paper list has issues.')

    if paper_base.get('affiliations') is None:
      paper_base['affiliations'] = []
    if paper_base.get('authors') is None:
      paper_base['authors'] = []

    for e in self._iterator:
      if e.get('pubName'):
        self._next_paper_base = e
        return self.format_output_paper(paper_base)

      if e.get('authors'):
        paper_base['authors'] += e['authors']

      if e.get('affiliations'):
        paper_base['affiliations'] += e['affiliations']

    self._next_paper_base = None
    return self.format_output_paper(paper_base)
