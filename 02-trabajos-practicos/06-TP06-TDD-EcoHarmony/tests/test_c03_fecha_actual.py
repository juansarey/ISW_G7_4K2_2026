"""C03 — Compra válida con visita en la fecha actual.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA02, CA05
- Tipo: Válida
- Condición: Cambiar la fecha por D0; parque abierto ese día.
- Comportamiento esperado: Aceptar la fecha actual. El resto de la solicitud
  permanece válido.
- Preparación sugerida: crear_solicitud(fecha_visita=fecha_actual)
- Motivo esperado: no corresponde (aceptación)

Tests previstos (nombres sugeridos):
- test_c03_acepta_visita_en_la_fecha_actual

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
