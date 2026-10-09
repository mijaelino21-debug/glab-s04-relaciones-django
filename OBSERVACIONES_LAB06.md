# OBSERVACIONES_LAB06.md

## Estructura de plantillas
La estructura utiliza un archivo base (`base.html`) que contiene el esqueleto común (head, scripts, header, footer) utilizando bloques (`{% block %}`) para permitir la personalización de las páginas hijas (`home.html`, `article_detail.html`, etc.). El uso de un parcial (`_article_card.html`) mediante `{% include %}` permite reutilizar la lógica de visualización de cada artículo en diferentes vistas (portada y categorías), asegurando coherencia y mantenimiento eficiente.

## Filtros y etiquetas de control
Se han utilizado:
- `{% for ... empty %}`: Control de bucles con caso base para cuando la colección está vacía.
- `{% include %}`: Inserción de parciales.
- `{% url %}`: Resolución dinámica de URLs a través de nombres.
- `{{ ...|date:"d M Y" }}`: Formateo de fechas.
- `{{ ...|truncatewords:25 }}`: Recorte de texto.
- `{{ ...|linebreaks }}`: Conversión de saltos de línea.

## Gestión de archivos estáticos y media
- `STATICFILES_DIRS`: Configurado para indicar dónde buscar archivos estáticos adicionales (CSS, JS) en desarrollo.
- `MEDIA_ROOT`: Configurado para definir la ruta donde se guardan los archivos subidos por los usuarios (`/media/articles/`). En desarrollo, Django sirve estos archivos automáticamente si `DEBUG=True`.

## Prueba de escapado automático XSS
Django, por defecto, escapa todo el contenido variable renderizado en las plantillas (`{{ variable }}`). Esto significa que caracteres especiales como `<` y `>` se convierten automáticamente en `&lt;` y `&gt;`. La prueba implementada inyecta un artículo con contenido `<script>alert(1)</script>` y verifica que, al ser renderizado en la página, aparezca como texto plano (`&lt;script&gt;alert(1)&lt;/script&gt;`) y no como un script ejecutable, confirmando que la protección contra ataques XSS está activa.
