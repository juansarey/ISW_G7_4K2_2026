"""C20 — Resumen de la compra confirmada.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA08, A03
- Tipo: Resultado
- Condición: Compra confirmada de dos entradas en D0 + 1. Variar pase regular y VIP
  (parametrizar).
- Comportamiento esperado: Resumen con dos entradas y D0 + 1. Total regular:
  $20.000; VIP: $30.000. Estado de pago según A02.
- Preparación sugerida: solicitud_base y crear_solicitud(tipo_pase=TipoPase.VIP)
- Motivo esperado: no corresponde (aceptación)

Tests previstos (nombres sugeridos):
- test_c20_informa_cantidad_fecha_y_total

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
