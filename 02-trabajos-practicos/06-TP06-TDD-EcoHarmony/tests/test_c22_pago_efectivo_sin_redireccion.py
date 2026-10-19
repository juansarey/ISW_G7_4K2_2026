"""C22 — Pago en efectivo sin redirección.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA06, DD05
- Tipo: Interacción
- Condición: Solicitud válida con efectivo.
- Comportamiento esperado: Confirmar compra con pago pendiente en boletería,
  solicitar correo y no redirigir al proveedor de tarjeta.
- Preparación sugerida: solicitud_base
- Motivo esperado: no corresponde (aceptación)

Tests previstos (nombres sugeridos):
- test_c22_efectivo_no_solicita_redireccion_de_pago

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
