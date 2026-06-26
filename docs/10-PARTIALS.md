# utilisation de templates partiels

## procédure

1. vous observez des structure HTML qui se répètent
2. en faire un fichier partial.html
3. le squelette HTML est entouré de 

```html
{% partialdef <partial_name> %}
    {{ var }}
{% endpartialdef <partial_name> %}
```

4. injecter le partial dans un template

```html
<div>
    {% with <partial_var>=<template_var> %}
        {% include partial.html#partial_name %}
    {% endwith %}
    ...
</div>
```