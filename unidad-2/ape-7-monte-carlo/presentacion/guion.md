# Guion del video: APE 7, método de Monte Carlo

Duración objetivo: 10 minutos. Unas 130 palabras por minuto, hablando tranquilo.
Las frases entre corchetes son indicaciones, no se leen.

---

## 1. Portada (0:00 a 0:40)

Hola, soy Alejandro Padilla, de Computación, ciclo 5. En este video presento la práctica 7 de Simulación: estimación de resultados mediante el método de Monte Carlo.

La idea es usar experimentos al azar para calcular dos cosas: el valor de π y la probabilidad de que dos dados sumen 7. Lo programé en Python y en Java, y al final comparo los dos lenguajes.

---

## 2. ¿Se puede calcular π lanzando puntos? (0:40 a 1:30)

Empiezo con una pregunta: ¿se puede calcular π lanzando puntos al azar? Parece raro, pero sí se puede.

Esa es la idea del método de Monte Carlo: repetir muchas veces un experimento al azar y contar cuántas veces pasa lo que nos interesa. Si lo repetimos suficientes veces, esa proporción se acerca al valor real.

No necesitamos fórmulas complicadas: solo números al azar y contar.

---

## 3. Modelo 1: π con el círculo (1:30 a 2:30)

[Señalar la figura del círculo.]

Imaginen un patio cuadrado con una piscina redonda en el medio, que toca los cuatro bordes. Si llueve, cada gota cae en un lugar al azar: algunas en la piscina y otras en las esquinas.

El patio mide 2 por 2, o sea 4. La piscina, un círculo de radio 1, mide π. Entonces la piscina ocupa π de 4, cerca del 78 %, y más o menos esa parte de las gotas cae dentro.

Yo hice lo mismo con puntos al azar. Con un millón de puntos, 785 487 cayeron dentro del círculo, los azules de la figura. Eso es 0.785487; lo multiplico por 4 y da 3.141948, casi exactamente π.

Esa es la fórmula de la guía: π es aproximadamente 4 por Nc sobre N, donde Nc son los puntos dentro y N el total.

---

## 4. Modelo 2: dos dados que suman 7 (2:30 a 3:40)

El docente pidió además un modelo matemático elegido por nosotros. Yo elegí este: la probabilidad de que dos dados sumen 7.

Con dos dados hay 36 resultados posibles, todos igual de probables. Seis de ellos suman 7: uno y seis, dos y cinco, tres y cuatro, y sus inversos. Entonces la probabilidad exacta es 6 de 36, que es un sexto, más o menos 0.1667.

Para simular un dado tomo un número al azar entre 0 y 1, lo multiplico por 6, me quedo con la parte entera y le sumo 1. Por ejemplo, 0.5 por 6 es 3, y 3 más 1 da la cara 4. Así sale una cara del 1 al 6, todas con la misma probabilidad.

Después lancé los dos dados un millón de veces: 167 162 veces sumaron 7, o sea 0.167162, casi exactamente un sexto.

Lo elegí porque su valor exacto se conoce, así que puedo medir el error igual que con π, y porque se puede comprobar a mano contando los 36 casos.

---

## 5. Mismo generador, mismos números (3:40 a 4:40)

[Seguir el flujo de izquierda a derecha.]

¿De dónde salen los números al azar? La guía pide que las dos implementaciones produzcan la misma secuencia con los mismos parámetros. Por eso no usé el generador que trae cada lenguaje: Python y Java tienen generadores distintos y darían números distintos.

Programé uno propio, un generador congruencial lineal. Se parte de un número inicial, la semilla, que es 12345. Cada número nuevo se calcula a partir del anterior: a por el número anterior, más c, y se toma el residuo de dividir para m. Luego se divide para m para tener un número entre 0 y 1.

Usé las mismas constantes en los dos lenguajes. Por eso Python y Java producen exactamente la misma lista de números. Cada punto usa dos números seguidos, uno para x y otro para y; y cada lanzamiento usa dos, uno por dado.

---

## 6. Modelo, Vista y Controlador (4:40 a 5:30)

Los dos programas siguen la arquitectura Modelo, Vista, Controlador, igual en Python y en Java.

El modelo hace los cálculos: el generador, los dos experimentos, el error y el tiempo. La vista muestra las tablas en la consola y, en Python, las gráficas. El controlador recibe los parámetros, el tamaño de muestra y la semilla, ejecuta los experimentos y pasa los resultados a la vista.

Además, el código tiene 18 pruebas automáticas. Una de ellas comprueba que Java cuente exactamente los mismos aciertos que Python.

---

## 7. Resultados de π (5:30 a 6:30)

Corrí cada experimento con 1 000, 10 000, 100 000 y 1 000 000 de puntos, como pide la guía.

Con 1 000 puntos salió 3.188. Con 10 000, 3.1516. Con 100 000, 3.1332. Y con un millón de puntos salió 3.141948, con un error de apenas 0.000355.

O sea, en general, más puntos dan una estimación más cercana a π. Pero fíjense que de 10 000 a 100 000 casi no mejoró. Eso lo explico en la siguiente diapositiva.

---

## 8. El error baja, pero no siempre (6:30 a 7:40)

[Señalar las dos gráficas.]

Esta gráfica muestra el error según el tamaño de muestra, a la izquierda para π y a la derecha para los dados. La línea punteada es el error que se espera en promedio.

En general el error baja, pero no en cada paso. En los dados, con un millón de lanzamientos el error fue 0.000495, mayor que con 100 000, que fue 0.000203. Los lanzamientos extra también tienen su propio azar.

Lo importante es que bajar el error cuesta mucho: para tener un error 10 veces más pequeño se necesitan unas 100 veces más muestras.

---

## 9. Python frente a Java (7:40 a 8:40)

En los ocho casos, cuatro tamaños por dos modelos, Python y Java contaron los mismos aciertos. Por ejemplo, con un millón de puntos, los dos contaron 785 487 puntos dentro del círculo. Entonces dieron la misma estimación y el mismo error.

Lo único que cambió fue el tiempo. Con un millón de puntos, Python tardó 0.519 segundos y Java 0.011 segundos: Java fue unas 46 veces más rápido. Esto pasa porque Java traduce a código de máquina las partes que más se repiten mientras el programa corre, y Python interpreta cada instrucción cada vez.

---

## 10. Lo que aprendí (8:40 a 10:00)

Para cerrar, tres ideas.

Primero: Monte Carlo estima un valor contando aciertos al azar. Con un millón de muestras estimé π en 3.141948 y la probabilidad de sumar 7 en 0.167162, muy cerca de un sexto.

Segundo: más muestras bajan el error en general, pero cuestan tiempo, y no garantizan que cada corrida sea mejor.

Tercero: si se usa el mismo generador y la misma semilla, los resultados son iguales en cualquier lenguaje, y así la comparación de tiempos es justa.

El código y el informe están en el repositorio de la asignatura. Gracias por su atención.
