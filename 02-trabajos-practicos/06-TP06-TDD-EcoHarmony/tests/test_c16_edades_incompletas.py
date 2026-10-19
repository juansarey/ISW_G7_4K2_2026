"""C16 — Rechazo por edades incompletas.

Estado: PENDIENTE. Escribir el test primero y registrar la evidencia Red en
docs/REGISTRO_TDD.md antes de modificar el código de producción.

- Criterios / decisiones: CA01
- Tipo: Rechazo
- Condición: Dos entradas y edad informada para un solo visitante.
- Comportamiento esperado: Rechazar por no contar con la edad de cada visitante.
- Preparación sugerida: crear_solicitud(edades=(24,))
- Motivo esperado: MotivoRechazo.EDADES_INCOMPLETAS

Tests previstos (nombres sugeridos):
- test_c16_rechaza_si_falta_la_edad_de_un_visitante

Ver tests/test_c01_compra_valida_efectivo.py como ejemplo de estructura
(preparación, ejecución y verificación) y tests/conftest.py para las fixtures.
"""
