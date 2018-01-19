# coding=utf-8
# Python imports
# Django imports
from django.core.paginator import Paginator


# Third party app imports
# Local app imports


# Heredo del paginador estandar para añadirle un page_ranges limitando lo que quiero ver en la web
class PaginatorWithPageRange(Paginator):
    
    # Constructor
    def __init__(self, object_list, per_page, limite_paginas):
        super(PaginatorWithPageRange, self).__init__(object_list, per_page)
        # Control del número de páginas a mostrar en las templates
        self.limite_paginas = limite_paginas
        self.range = range(1, self.num_pages + 1)
        if self.num_pages > limite_paginas:
            self.range = range(1, limite_paginas)
    
    # Obtener página
    def page(self, number):
        # Crear el rango de enlaces a mostrar en el paginador
        if self.num_pages > 4:
            try:
                actual = int(number)
            except Exception:
                actual = 1
            # Estamos en la primera página
            if actual == 1:
                self.range = range(1, self.limite_paginas)
            # Estamos en la última página
            elif actual == self.num_pages:
                self.range = range(self.num_pages - 3, self.num_pages + 1)
            # Si podemos hacer un rango desde -1 a + 2 (caso normal)
            elif actual + 2 < self.num_pages:
                self.range = range(actual - 1, actual + 3)
            # Si no deberíamos poder hacer un rango de -2 a + 1
            else:
                self.range = range(actual - 2, actual + 2)
        # Llamo a la implementación original
        return super(PaginatorWithPageRange, self).page(number)
