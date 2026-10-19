"""C24 — La redirección no acredita el pago.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: DD05, A02
- Tipo: Interacción
- Condición: Redirección solicitada y todavía sin confirmación del pago.
- Comportamiento esperado: Mantener compra y pago pendientes, sin solicitar correo.
  La redirección no acredita el pago.
- Preparación sugerida: crear_solicitud(forma_pago=FormaPago.TARJETA)
- Motivo esperado: no corresponde (aceptación)

Tests previstos (nombres sugeridos):
- test_c24_redireccion_sin_aprobacion_no_envia_correo

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
