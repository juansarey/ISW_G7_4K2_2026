"""C08 — Compra con pase VIP.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA01, A03
- Tipo: Válida
- Condición: Cambiar el tipo de pase a VIP.
- Comportamiento esperado: Aceptar y conservar el pase VIP. Para dos entradas, total
  de $30.000 según A03.
- Preparación sugerida: crear_solicitud(tipo_pase=TipoPase.VIP)
- Motivo esperado: no corresponde (aceptación)

Tests previstos (nombres sugeridos):
- test_c08_acepta_y_conserva_pase_vip

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
