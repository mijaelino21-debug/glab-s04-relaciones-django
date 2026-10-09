# OBSERVACIONES

### 1) Configuración del admin
Se configuró el panel administrativo para los modelos `Genre`, `Person`, `Movie` y `Rating`:
- **Genre & Person:** Listado simple y búsqueda por nombre.
- **Movie:**
    - `list_display` incluye campos calculados (`genre_list`, `avg_rating`).
    - `list_filter` por géneros y año.
    - `search_fields` por título y director.
    - `filter_horizontal` para la relación muchos a muchos con `Genre`.
    - `readonly_fields` (`created_at`, `updated_at`).
    - `inlines` para mostrar `RatingInline` dentro de `Movie`.
- **Rating:** Listado con filtrado por puntuación y búsqueda.

### 2) Reparto de roles
| Rol | Acciones permitidas | Gestión de Usuarios |
| :--- | :--- | :--- |
| **Superusuario** | Control total (CRUD completo) | Sí |
| **Grupo "editores"** | Ver, añadir, cambiar películas y valoraciones. No eliminar | No |

**Justificación:** El superusuario requiere control administrativo total. El grupo de "editores" tiene acceso operativo (gestión de contenido) pero sin capacidad de destrucción de datos (eliminar) ni de gestión administrativa de cuentas de usuario, garantizando la integridad y seguridad básica.

### 3) Relaciones (CASCADE vs PROTECT)
- **`Rating.movie` (CASCADE):** Un rating es dependiente del contexto de la película. Si la película es eliminada, sus valoraciones pierden sentido y deben eliminarse automáticamente para mantener la integridad referencial.
- **`Book.author` (PROTECT):** Se utiliza `PROTECT` para evitar que un autor sea eliminado si todavía tiene libros registrados en el sistema. Esto previene la pérdida accidental de datos de libros vinculados a autores.

### 4) Panel vs Vista Pública
- **Panel administrativo:** Muestra toda la información, incluyendo campos de auditoría, y permite la gestión total de los datos.
- **Vista pública (recomendaciones):** Exige una lógica de negocio propia (solo mostrar películas con al menos una valoración, ordenadas por promedio de calificación) para asegurar una experiencia de usuario relevante.

### 5) Datos de prueba
Se cuenta con el usuario `editor_test` con contraseña de desarrollo, configurado exclusivamente para pruebas en entornos locales.
