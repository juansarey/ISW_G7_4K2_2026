> **Clase:** 15/09/2026 | **Tema:** User Stories, Gestión de Producto y Estimaciones (práctico)

> Hoy es el ultimo evento donde hacemos estas practicas, la proxima clase es el evento de SCRUM
> ESTANDARES: _con cursiva pongo las correcciones, suelen ser agregados_
# Caso Body Painting
## User Stories
### US del Cliente
- Iniciar sesion ✅
- Crear cuenta (usar datos personales)  
- Agregar productos al carrito
- Visualizar carro de compras
- Editar carro de compras
- Agregar domicilio de envio(?)
- Editar domicilio de envio(?)
- Seleccionar forma de pago
- Confirmar pago
- Confirmar pedido
- Realizar reclamo a bodypainting
- Ingresar cupon de descuento
### US del Vendedor
- Visualizar stock de productos
- Editar producto
- Registrar producto nuevo
- Eliminar producto
- Registrar kits de producto
- Eliminar kits de producto
- Editar kits de producto
- Visualizar reporte de kits
- Visualizar reporte de stock
- Realizar carga masiva de productos (csv o excel)
- Enviar mail a cliente con información sobre el pedido
- Visualizar el estado del pedido
- Cancelar entrega de pedido
- Registrar cupon de descuento
- Generar reporte de productos + vendidos, etc..
## MVP
### US del MVP:
##### Cliente:
- Iniciar sesion ❌
- Crear cuenta (usar datos personales) ❌
- _Registrar cliente_
- _Visualizar productos_
- Agregar productos al carrito ✅
- Visualizar carro de compras ✅
- Agregar domicilio de envío ✅
- Seleccionar forma de pago ❌
- Confirmar pedido ❌
- _Confirmar pago en efectivo_
##### Vendedor:
- Registrar venta ❌
- _Visualizar estado de pedido_
##### Admin de Productos:
- Visualizar stock de productos ❌ (Se entiende que en consultar producto se puede ver el stock también, pero tampoco esta mal si se pone)
- Editar producto 
- Registrar producto ✅
- Eliminar producto
- _Consultar producto_
##### **US Canonica: Registrar cliente**
  
> Aca no identificamos bien los roles, poruqe era Cliente, Vendedor, y Admin de Productos, asi que reacomode para que queden bien las US por rol
> PRO-TIP: Siempre separar las US por roles, asi es mas facil de verlas digamos y darse cuales van
## US: Reclamar reembolso del pedido
_"Como cliente quiero poder reclamar reembolso para recuperar el dinero invertido en el producto"_
#### Criterios de Aceptación
- Haber recibido el pedido
- Tienen que haber pasado menos de 5 dias habiles de haber recibido el pedido
#### Casos de Prueba
- Puedo reclamar el reembolso hasta 5 días despues de ser entregado = PASA
- Puedo reclamar el reembolso despues de 5 dias de ser entregado = FALLA
- Puedo reclamar el reembolso antes de recibir el pedido = FALLA
#### Estimación -> SON 3 LOS PUNTOS
## US: Cargar partida de productos en archivo .xlsx

###### Correcciones y cosas de clase
- TODA la parte de envio es un feature aparte, osea NO VA AL MVP
- NO se contemplan los reportes para el MVP
- NO incluye la de reclamos
- Para estimar hacemos: 1. Tamaño (en estimaciones agiles usamos peso), 2. Esfuerzo (lo medimos en **horas persona** lineales, cuanto tiempo me toma hacer una tarea), 3. Tiempo (dias, semanas, meses, etc..) y Costo
- **Diferencia entre complejidad y esfuerzo:** en la Complejidad hablamos de lo que A VOS te genera cierta complejidad en esa US, y Esfuerzo no hace falta que pongas tipo "Para mi va a tomar 10 horas blabla" la idea es que pongas cuanto tiempo te va a tomar. Por ejemplo, hacer un formulario, es de baja complejidad, aunque tenga 100 campos, pero si tiene 100 campos entonces va a requerir esfuerzo porque son 100 campos justamente. Generalmente una tarea mas compleja requiere mas esfuerzo, pero no siempre es "lineal" digamos.