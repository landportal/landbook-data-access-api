from model import models
from sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy.orm import class_mapper

# lets find all the mappers in our model
mappers = []
for attr in dir(models):
    if attr[0] == '_': continue
    try:
        cls = getattr(models, attr)
        mappers.append(class_mapper(cls))
    except:
        pass

# pass them to the function and set some formatting options
graph = create_uml_graph(mappers,
    show_operations=False,  # not necessary in this case
    show_multiplicity_one=True,  # some people like to see the ones, some don't
    font='Calibri'
)
graph.write('schema.svg',format='svg') # write out the file