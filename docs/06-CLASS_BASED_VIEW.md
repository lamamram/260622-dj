# Vues générique avec classes Django

## Introduction

* classes génériques dans `django.views.generic`

## exemples de vues génériques

### ListView

```python
from django.views.generic import ListView

class TrucListView(ListView):
    model = Truc
    template_name = 'truc_list.html'
    context_object_name = 'trucs'
    paginate_by = 10
```