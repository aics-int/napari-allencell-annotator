import json
from view.annotator_view import AnnotatorView

with open('sample.json') as s:
    data = json.load(s)

view = AnnotatorView(data)
