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

### DetailView

```python
from django.views.generic import DetailView

class TrucDetailView(DetailView):
    model = Truc
    template_name = 'truc_detail.html'
    context_object_name = 'truc'
```

```html
<header class="py-5 bg-light border-bottom mb-4">
    <div class="container px-5">
        <h1 class="fw-bolder"></h1>
    </div>
</header>
```

```html
<div class="container px-5 my-5">
    <div class="card">
        <div class="card-body">
            <dl class="row">
                <dt class="col-sm-3">Name</dt>
                <dd class="col-sm-9"></dd>

                <dt class="col-sm-3">Type</dt>
                <dd class="col-sm-9"></dd>

                <dt class="col-sm-3">Number</dt>
                <dd class="col-sm-9"></dd>

                <dt class="col-sm-3">Balance</dt>
                <dd class="col-sm-9"></dd>

                <dt class="col-sm-3">Overdraft</dt>
                <dd class="col-sm-9"></dd>

                <dt class="col-sm-3">Credit Rate</dt>
                <dd class="col-sm-9"></dd>

            </dl>
            <a href="{% url 'account_list' %}" class="btn btn-secondary">Back to Accounts</a>
        </div>
    </div>
</div>
```