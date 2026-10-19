"""C23 — Un rechazo no produce efectos.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: DD02
- Tipo: Interacción
- Condición: Solicitud con once entradas; dependencias sin acciones previas.
- Comportamiento esperado: Rechazar y comprobar ausencia de solicitudes de pago,
  correo y registro de compra finalizada.
- Preparación sugerida: crear_solicitud(cantidad_entradas=11, edades=(30,) * 11)
- Motivo esperado: MotivoRechazo.CANTIDAD_EXCEDE_MAXIMO

Tests previstos (nombres sugeridos):
- test_c23_rechazo_no_produce_pago_correo_ni_registro

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
