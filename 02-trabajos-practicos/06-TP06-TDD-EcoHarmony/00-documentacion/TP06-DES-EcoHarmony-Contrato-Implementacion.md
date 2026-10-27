# Contrato de implementación — Comprar entradas

Interfaz pública compartida por la lógica, la interfaz web y los tests. Los cambios
incompatibles se coordinan con el equipo antes de aplicarse (regla 6).

**Estado:** versión inicial. Las secciones marcadas como *propuesta* deben
confirmarse cuando se construyan los casos que las usan.

## 1. Módulos y nombres públicos

| Módulo | Nombres públicos | Responsabilidad |
|---|---|---|
| `ecoharmony.modelos` | `Usuario`, `SolicitudCompra`, `Compra`, `ResultadoCompra`, `TipoPase`, `FormaPago`, `EstadoCompra`, `EstadoPago`, `EstadoCorreo`, `MotivoRechazo` | Tipos del dominio y del resultado |
| `ecoharmony.tarifas` | `MAXIMO_ENTRADAS`, `TARIFAS_POR_PASE`, `calcular_total` | Regla CA07 y tarifas A03 |
| `ecoharmony.dependencias` | `Reloj`, `Calendario`, `ServicioPago`, `ServicioCorreo`, `RepositorioCompras`, `ErrorServicioPago`, `ErrorServicioCorreo` | Interfaces de las dependencias (DD01) |
| `ecoharmony.servicio_compras` | `ServicioCompras` | Validación y coordinación de la compra |
| `ecoharmony.entrada` | `convertir_solicitud` | Límite de entrada: texto/JSON → `SolicitudCompra` |
| `ecoharmony.simulados` | `RelojFijo`, `CalendarioParque`, `PagoSimulado`, `CorreoSimulado`, `RepositorioComprasEnMemoria` | Servicios de la demostración (A01, A04) |
| `ecoharmony.web` | `crear_app` | Interfaz web (Flask) |

Los dobles de prueba están en `tests/dobles.py` y no se importan desde producción.

## 2. Solicitud

```python
@dataclass(frozen=True)
class SolicitudCompra:
    usuario: Usuario  # Usuario(nombre_usuario, correo, registrado)
    fecha_visita: date | None  # None = ausente (C15)
    cantidad_entradas: int | None  # None = ausente (C18)
    edades: tuple[int, ...]  # () = ninguna edad informada
    tipo_pase: TipoPase | None  # None = ausente (C17)
    forma_pago: FormaPago | None  # None = ausente (C13)
```

- Un campo **ausente** se representa con `None` (o `()` para las edades).
- Un **formato inválido** (texto que no es fecha, número u opción admitida) se detecta
  en `ecoharmony.entrada`; la lógica de compra solo recibe tipos ya convertidos.
- Un **rechazo de negocio** lo decide `ServicioCompras.comprar`.

## 3. Resultado

`ServicioCompras.comprar(solicitud) -> ResultadoCompra` es el único mecanismo para
comunicar el resultado. No se usan excepciones, booleanos sueltos ni mensajes
impresos para representar un rechazo.

| Campo | Aceptada | Rechazada |
|---|---|---|
| `aceptada` | `True` | `False` |
| `compra` | `Compra` registrada | `None` |
| `motivo` | `None` | `MotivoRechazo` |
| `url_redireccion` | URL de la pasarela solo si la forma de pago es tarjeta | `None` |

`Compra` conserva los valores validados: `id_compra`, `usuario`, `fecha_visita`,
`cantidad_entradas`, `edades`, `tipo_pase`, `forma_pago`, `total` (`Decimal`),
`estado_compra`, `estado_pago` y `estado_correo`.

En la compra confirmada, el resultado expone cantidad, fecha de visita, tipo de
pase y total calculado con A03. Para dos entradas el total es `Decimal("20000")`
con pase regular y `Decimal("30000")` con pase VIP; la forma y el estado de pago
corresponden a A02 (C20).

## 4. Motivos de rechazo

| Identificador | Caso | Detectado en |
|---|---|---|
| `USUARIO_NO_REGISTRADO` | C14 | servicio |
| `FECHA_AUSENTE` | C15 | servicio |
| `FECHA_FORMATO_INVALIDO` | C27 | entrada |
| `FECHA_PASADA` | C10 | servicio |
| `PARQUE_CERRADO` | C11 | servicio |
| `CANTIDAD_AUSENTE` | C18 | servicio |
| `CANTIDAD_INVALIDA` | C25 | servicio (cero/negativa) y entrada (no entera) |
| `CANTIDAD_EXCEDE_MAXIMO` | C12, C23 | servicio |
| `EDADES_INCOMPLETAS` | C16 | servicio |
| `EDAD_INVALIDA` | C28 | servicio (negativa) y entrada (no entera) |
| `TIPO_PASE_AUSENTE` | C17 | servicio |
| `TIPO_PASE_INVALIDO` | C26 | entrada |
| `FORMA_PAGO_AUSENTE` | C13 | servicio |
| `FORMA_PAGO_INVALIDA` | C26 | entrada |
| `ERROR_PAGO` | C21 | servicio (fallo al iniciar el pago, A04) |

La interfaz traduce cada identificador a un mensaje en `ecoharmony/web/mensajes.py`.

### Política ante varios datos inválidos (*propuesta*)

Se devuelve **un solo motivo**: el primero que falle en este orden: usuario →
fecha (ausente, pasada, cerrada) → cantidad (ausente, inválida, máximo) → edades
(incompletas, inválidas) → tipo de pase → forma de pago. Los casos individuales
cambian un único dato, por lo que no dependen de este orden.

## 5. Estados y transiciones

| Situación | `estado_compra` | `estado_pago` | `estado_correo` | Casos |
|---|---|---|---|---|
| Efectivo aceptado | `CONFIRMADA` | `PENDIENTE_BOLETERIA` | `ENVIADO` | C01, C22 |
| Tarjeta aceptada, pasarela abierta | `PENDIENTE` | `PENDIENTE_PASARELA` | `NO_SOLICITADO` | C02, C24 |
| Tarjeta aprobada | `CONFIRMADA` | `APROBADO` | `ENVIADO` o `CORREO_PENDIENTE` | C19 |
| Tarjeta rechazada o cancelada | `CANCELADA` | `RECHAZADO` | `NO_SOLICITADO` | A02 |
| Fallo del correo | se conserva | se conserva | `CORREO_PENDIENTE` | C19 |
| Fallo al iniciar el pago | sin compra confirmada (`aceptada=False`, `ERROR_PAGO`) | — | — | C21 |

Transiciones permitidas:

- `PENDIENTE` → `CONFIRMADA` (pago aprobado) o `CANCELADA` (pago rechazado o cancelado).
- `PENDIENTE_PASARELA` → `APROBADO` o `RECHAZADO`.
- `NO_SOLICITADO` → `ENVIADO` o `CORREO_PENDIENTE`; `CORREO_PENDIENTE` → `ENVIADO` (reintento).
- `CONFIRMADA` y `CANCELADA` son estados finales.

## 6. Dependencias

```python
class Reloj(Protocol):
    def hoy(self) -> date: ...


class Calendario(Protocol):
    def esta_abierto(self, fecha: date) -> bool: ...


class ServicioPago(Protocol):
    # Devuelve la URL de la pasarela. Lanza ErrorServicioPago si falla.
    def iniciar_pago_tarjeta(self, id_compra: str, monto: Decimal) -> str: ...


class ServicioCorreo(Protocol):
    # Lanza ErrorServicioCorreo si falla.
    def enviar_confirmacion(self, compra: Compra) -> None: ...


class RepositorioCompras(Protocol):
    def guardar(self, compra: Compra) -> None: ...
    def obtener(self, id_compra: str) -> Compra | None: ...
```

`ServicioCompras(reloj, calendario, servicio_pago, servicio_correo, repositorio)`
recibe todas las dependencias en el constructor.

## 7. Operaciones de pago y correo

`registrar_resultado_pago` procesa el resultado de la pasarela simulada:

```python
ServicioCompras.registrar_resultado_pago(id_compra: str, aprobado: bool) -> ResultadoCompra
ServicioCompras.reintentar_correo(id_compra: str) -> ResultadoCompra
```

Para `registrar_resultado_pago`, `aceptada=True` significa que la notificación se
procesó; no significa necesariamente que el pago se aprobó. El resultado del pago
se expresa mediante los estados de la compra. Esta interpretación es propia de
esta operación y no cambia el significado de `ServicioCompras.comprar`.

La operación solo acepta compras con tarjeta existentes y en estado
`PENDIENTE` / `PENDIENTE_PASARELA`. Un identificador inexistente, una compra que no
sea con tarjeta o una transición incompatible produce `ValueError`. La repetición
de la misma notificación ya procesada es idempotente: no duplica el correo ni
reinicia el pago; una notificación opuesta a un resultado final produce
`ValueError`.

Una aprobación confirma la compra y el pago, guarda esos estados y solicita el
correo una sola vez. Si el servicio lanza `ErrorServicioCorreo`, se conservan la
compra confirmada y el pago aprobado, y el estado de correo queda
`CORREO_PENDIENTE`. Repetir la notificación no reintenta el correo; esa recuperación
explícita corresponde a C30. Un rechazo/cancelación deja la compra
`CANCELADA` y el pago `RECHAZADO`, sin solicitar correo (A02; C29 mantiene sus
pruebas propias).

`reintentar_correo` solo acepta una compra existente con estado de correo
`CORREO_PENDIENTE`. Si el identificador no existe o el correo no está pendiente,
produce `ValueError`. El reintento solicita únicamente el correo y devuelve la
compra; si vuelve a fallar, conserva `CORREO_PENDIENTE`, y si tiene éxito lo cambia
a `ENVIADO`. No inicia otro pago ni crea otra compra (C30).

## 8. API web

| Método y ruta | Descripción |
|---|---|
| `GET /` | Formulario de compra |
| `GET /api/configuracion` | Fecha simulada, usuarios simulados, tarifas y calendario |
| `POST /api/compras` | Recibe JSON con `usuario`, `fecha_visita` (`AAAA-MM-DD`), `cantidad_entradas`, `edades`, `tipo_pase`, `forma_pago`; devuelve el `ResultadoCompra` serializado más `mensaje` |
| `GET /api/compras/<id>` | Estado de una compra |
| `GET /api/correos` | Bandeja del correo simulado |
| `GET /pasarela-simulada/<id>` | Página de la pasarela simulada (no es Mercado Pago) |
