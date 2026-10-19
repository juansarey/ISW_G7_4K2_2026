"""C25 — Cantidad no entera positiva (DG01).

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: DG01
- Tipo: Rechazo (decisión del grupo)
- Condición: Cantidad cero, negativa o no entera; una variación por ejecución
  (parametrizar). La cantidad no entera se rechaza en ecoharmony.entrada.
- Comportamiento esperado: Rechazar: se requieren entradas en cantidad entera
  positiva.
- Preparación sugerida: crear_solicitud(cantidad_entradas=0, edades=()) / -1 /
  convertir_solicitud con '2.5'
- Motivo esperado: MotivoRechazo.CANTIDAD_INVALIDA

Tests previstos (nombres sugeridos):
- test_c25_rechaza_cantidad_no_entera_positiva

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
