# Criterio de Lineas Base

## Objetivo y definicion

Una linea base representa un estado identificado y estable de uno o mas Items de Configuracion en un momento determinado. Sirve como referencia para controlar su evolucion posterior.

## Criterio de establecimiento

Se establece una linea base al alcanzar un hito academico relevante, cuando los CIs asociados:

- estan completos para el alcance definido;
- fueron revisados por el grupo;
- estan correctamente ubicados en el repositorio;
- respetan las reglas de nombrado;
- estan en condiciones de presentarse, evaluarse o utilizarse como base de actividades posteriores.

## Implementacion en Git

Las lineas base se representan mediante tags de Git sobre el commit que refleja el estado estable. El formato es `LB-<numero>-<descripcion>`, usando un numero correlativo de dos digitos.

Ejemplos: `LB-01-Configuracion-Inicial`, `LB-02-Requerimientos-EcoHarmony` y `LB-03-TDD-EcoHarmony`.

La primera linea base se crea una vez definida la estructura inicial, completa la documentacion SCM, incorporados los CIs disponibles y aprobado el estado por el grupo. Su identificador es `LB-01-Configuracion-Inicial`.

Despues de cada linea base, los CIs pueden continuar evolucionando mediante nuevos commits. Cada nuevo estado estable que cumpla este criterio genera una nueva linea base, sin modificar ni eliminar las anteriores.
