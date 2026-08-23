# Reglas de Nombrado de Items de Configuracion

## Directorios

Todos los directorios y subdirectorios usan el formato `<numero>-<descripcion>`, con numero de dos digitos. Los directorios de trabajos practicos usan `<numero>-TP<numero>-<tema>-<dominio>`.

Ejemplos: `00-SCM`, `01-reglas-materia`, `06-TP06-TDD-EcoHarmony`, `00-codigo-fuente` y `01-pruebas-automatizadas`.

No se crea un subdirectorio para un unico archivo: se guarda directamente en el directorio de nivel superior.

## Reglas generales para archivos

- No usar espacios, acentos ni caracteres especiales.
- Usar guiones medios (`-`) como separadores.
- Usar nombres breves y descriptivos.
- No incluir numeros de version ni calificativos de estado como `final` en el nombre.
- Mantener el nombre mientras represente el mismo CI; Git administra las versiones y modificaciones.

## Convenciones por tipo de CI

| Tipo | Formato |
| --- | --- |
| SCM | `SCM-<descripcion>.<extension>` |
| Reglas de materia | `REG-<descripcion>.<extension>` |
| Material teorico | `MAT-<tema>-<descripcion>.<extension>` |
| Material teorico por unidad | `MAT-U<numero>-<tema>-<descripcion>.<extension>` |
| Trabajo practico | `TP<numero>-<tipoCI>-<dominio>-<descripcion>.<extension>` |
| Investigacion grupal | `INV-<descripcion>.<extension>` |

Ejemplos: `SCM-Reglas-Nombrado.md`, `REG-Criterios-Evaluacion.pdf`, `MAT-U03-SCM-Gestion-Configuracion.pdf`, `TP09-TST-EcoHarmony-CasosPrueba.xlsx` e `INV-Informe-Final.pdf`.
