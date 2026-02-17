# Unit Primitives for Agents

Este módulo proporciona primitivas unitarias que permiten a los agentes (`otto-task-shadow`, `shadow-architect`, etc.) realizar operaciones básicas en el repositorio.

## Módulos

### `file_operations.py`
Operaciones con archivos:
- `create_file()` - Crear nuevos archivos
- `edit_file()` - Editar archivos existentes
- `delete_file()` - Eliminar archivos
- `read_file()` - Leer contenido de archivos

### `git_operations.py`
Operaciones con Git:
- `create_commit()` - Crear commits
- `push_branch()` - Hacer push a ramas
- `create_branch()` - Crear nuevas ramas
- `delete_branch()` - Eliminar ramas
- `get_current_branch()` - Obtener rama actual

### `merge_request_operations.py`
Operaciones con Merge Requests:
- `create_merge_request()` - Crear MRs
- `update_merge_request()` - Actualizar MRs
- `merge_merge_request()` - Mergear MRs
- `close_merge_request()` - Cerrar MRs

## Uso

```python
from primitives import (
    create_file,
    create_commit,
    push_branch,
    create_merge_request
)

# Crear un archivo
create_file("src/new_file.py", "print('Hello')")

# Hacer commit
create_commit("feat: add new file")

# Hacer push
push_branch("feature-branch")

# Crear MR
success, mr_iid = create_merge_request(
    source_branch="feature-branch",
    target_branch="main",
    title="New Feature"
)
```

## Requisitos

- Git instalado y configurado
- GitLab CLI (`glab`) instalado para operaciones de MR
- Acceso al repositorio
