"""C14 — Rechazo por usuario no registrado.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA09
- Tipo: Rechazo
- Condición: Visitante no registrado con los demás datos válidos.
- Comportamiento esperado: Rechazar por la condición de registro del usuario.
- Preparación sugerida: crear_solicitud(usuario=replace(usuario_registrado,
  registrado=False))
- Motivo esperado: MotivoRechazo.USUARIO_NO_REGISTRADO

Tests previstos (nombres sugeridos):
- test_c14_rechaza_usuario_no_registrado

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
