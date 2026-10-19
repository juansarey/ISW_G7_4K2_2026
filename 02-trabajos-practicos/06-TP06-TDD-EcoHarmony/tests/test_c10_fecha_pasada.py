"""C10 — Rechazo por fecha pasada.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA02
- Tipo: Rechazo
- Condición: Fecha D0 - 1; parque abierto ese día.
- Comportamiento esperado: Rechazar porque la visita es anterior a la fecha actual.
- Preparación sugerida: crear_solicitud(fecha_visita=fecha_actual -
  timedelta(days=1))
- Motivo esperado: MotivoRechazo.FECHA_PASADA

Tests previstos (nombres sugeridos):
- test_c10_rechaza_fecha_anterior_a_la_actual

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
