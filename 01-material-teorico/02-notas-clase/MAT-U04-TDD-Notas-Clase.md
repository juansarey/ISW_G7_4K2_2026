> **Clase:** 06/10/2026 | **Tema:** TDD (Test Driven Development)

# TDD - Test Driven Development
> Van a estar las notas del parcial el 19

TDD vincula el testing con el desarollo. Hay que usar TDD para el TP. Hay que ejecutar las pruebas unitarias en caso de hacer bien el desarollo de TDD. Se hace con la herramienta que mas te guste, cualquier lenguaje de programación mientras funcione. ***Martes 20 de octubre se entrega este TP***. Tenes que ejecutar el software y las pruebas unitarias. Despues tenemos que probar la US de otro grupo. 
### ¿Que es TDD?
Es una practica para desarollar software donde el planteo es si primero pienso como voy a probar las cosas, diseño primero esas pruebas, y despues hago el software. Primero diseño el resultado de lo que quiero, por eso escribo primero las pruebas de resultado, y despues hago el software que pase esas pruebas. El ciclo de TDD es que yo diseño y despues hago las pruebas para pasar ese diseño. Diseñar -> Probar -> Refactor.
1. Escribo las pruebas
2. Desarrollo el software
3. Después pruebo y corrijo errores
### ¿Por que lo hacemos?
Para que el código sea mas robusto, en caso que las pruebas se rompan ya se a donde tengo que ir para corregir y que ande bien digamos. Las pruebas tienen que tener la cobertura de todo el código. Buscamos que sea mas seguro. Es para saber cuando esta terminado. Reducir la duplicidad, etc... (Revisar las ventajas en las filminas)
### La base de TDD
***Primero escribo las pruebas, escribo el código para que las pruebas pasen, y después hago el refactor.***
Y así lo tengo que hacer una y otra vez.
### Patrones de TDD
Los test tienen que ser:
- Cortos
- Tienen que esta documentados
- Tienen que funcionar con APIs? algo asi
- Hay que ponerle de nombre "test" al comienoz
- Agruparlos en listas de test
- etc..
## Refactoring
El código tiene que seguir haciendo el mismo pero tiene que estar bien documentado, no tiene que estar duplicado, tiene que ser mas simple, etc.. Hacemos refactor porque a medida que metemos cambios el código se vuelve mas complicado, entonces por eso existe el refactor.
### ¿Como hacer refactoring?
1. Arranca con pruebas que fallas
2. Escribimos el código mínimo para que pasen las pruebas
3. Una vez que pasen hago el refactor hasta que vuelvan a fallar
4. Repito
# Practico de TDD
 Para arrancar a hacer una prueba ponemos `def` para definir la función que vamos a definir.
 Hay como que setear el sistema para las pruebas que vamos a hacer.

Voy a hacer los test con mi amigo Maxi que no es Tabares y Octa
### **US: Comprar entradas**
*"Como visitante*
*Quiero comprar una entrada*
*Para asegurar mi visita al parque"*

Como estamos usando TDD (Test Driven Development) primero tenemos que hacer los test y despues tenemos que hacer el codigo en base a ellos, para que el codigo funcione para que pasen los test, aca van los test que quiero que pase:
Probar comprar una entrada indicando la fecha de visita dentro de los días disponibles, una cantidad de entradas menor a 10, la edad de todos los visitantes, el tipo de pase, la forma de pago con tarjeta mediante Mercado pago y recepción del mail de confirmación (pasa) - Probar comprar entradas sin seleccionar forma de pago (falla) - Probar comprar entradas ingresando una fecha de visita en la cual el parque se encuentra cerrado (falla) - Probar comprar entradas ingresando una cantidad de entradas mayor a 10 (falla

La estructura que quiero que uses es:
