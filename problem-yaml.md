# problem.yaml — Referencia de configuración

Cada problema debe tener un archivo `problem.yaml` en su carpeta raíz. Este archivo define los metadatos que se usan al subir el problema a OmegaUp con `omegaup upload`.

`omegaup create` genera el archivo automáticamente con un flujo interactivo. Puedes editarlo manualmente en cualquier momento.

---

## Ejemplo completo

```yaml
alias: suma-dos-numeros
title: Suma de Dos Números
source: OMI Yucatán 2025
time_limit: 1000
memory_limit: 256
visibility: private
type: normal
validator: token
languages: cpp17,cpp20
tags:
  - name: math
    public: true
  - name: easy
    public: false
```

---

## Campos

### `alias`

Identificador único del problema en OmegaUp. Aparece en la URL: `omegaup.com/arena/problem/<alias>/`.

- Solo letras minúsculas, números y guiones.
- Debe ser único en toda la plataforma.
- No se puede cambiar una vez publicado el problema.

```yaml
alias: suma-dos-numeros
```

---

### `title`

Nombre visible del problema en la plataforma.

```yaml
title: Suma de Dos Números
```

---

### `source`

Origen o edición del problema (concurso, año, etc.). Puede dejarse vacío.

```yaml
source: OMI Yucatán 2025
source:          # vacío = sin fuente
```

---

### `time_limit`

Tiempo máximo de ejecución por caso, en **milisegundos**.

```yaml
time_limit: 1000    # 1 segundo
time_limit: 3000    # 3 segundos
```

---

### `memory_limit`

Memoria máxima permitida, en **megabytes**.

```yaml
memory_limit: 256    # 256 MB
```

---

### `visibility`

Controla quién puede ver el problema.

| Valor | Descripción |
|-------|-------------|
| `private` | Solo el autor (default recomendado mientras se desarrolla) |
| `public` | Visible para todos en OmegaUp |

```yaml
visibility: private
visibility: public
```

---

### `type`

Define si el problema acepta envíos de código o es una lectura sin envíos.

| Valor | Descripción |
|-------|-------------|
| `normal` | Problema estándar — acepta código en los lenguajes configurados |
| `lectura` | Lectura sin envíos — OmegaUp ignora el campo `languages` |

```yaml
type: normal
type: lectura
```

> Al usar `type: lectura`, el campo `languages` se ignora al subir: OmegaUp recibe `languages=""` automáticamente.

---

### `validator`

Método que usa OmegaUp para comparar la salida del programa con la salida esperada.

| Valor | Descripción |
|-------|-------------|
| `token` | Compara token por token, sensible a mayúsculas (default) |
| `token-caseless` | Compara token por token, ignora mayúsculas/minúsculas |
| `literal` | Comparación exacta byte a byte |
| `custom` | Usa el archivo `validator.cpp` incluido en el problema |

```yaml
validator: token
validator: custom    # requiere validator.cpp en la carpeta
```

> Si creas el problema con `omegaup create --validator`, el default de `validator` es `custom`.

---

### `languages`

Lenguajes de programación permitidos para los envíos, separados por comas.

Solo aplica cuando `type: normal`. Si `type: lectura`, este campo se ignora.

Valores comunes en OmegaUp:

| Código | Lenguaje |
|--------|----------|
| `cpp17` | C++17 |
| `cpp20` | C++20 |
| `java` | Java |
| `py3` | Python 3 |
| `c` | C |

```yaml
languages: cpp17,cpp20
languages: cpp17,cpp20,java,py3
```

---

### `tags`

Lista de etiquetas del problema. **Requerido:** al menos una tag debe tener `public: true`.

```yaml
tags:
  - name: math         # nombre de la etiqueta
    public: true       # visible para todos los usuarios
  - name: easy
    public: false      # visible solo para el autor
```

> OmegaUp no permite subir un problema sin al menos una etiqueta pública.

---

## Campos calculados automáticamente

Estos valores **no van en el YAML** — `omegaup upload` los calcula solo:

| Campo | Cálculo |
|-------|---------|
| `output_limit` | Tamaño del `.out` más grande en `cases/` + 1000 bytes |

---

## Campos requeridos vs opcionales

| Campo | Requerido para upload |
|-------|-----------------------|
| `alias` | Sí |
| `title` | Sí |
| `source` | No (puede estar vacío) |
| `time_limit` | Sí |
| `memory_limit` | Sí |
| `visibility` | Sí |
| `type` | Sí |
| `validator` | Sí |
| `languages` | Sí (ignorado si `type: lectura`) |
| `tags` | Sí (mínimo una pública) |
