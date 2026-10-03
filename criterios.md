# Criterios para escribir las preguntas

Estos criterios valen para cualquier banco nuevo y para cualquier cambio a uno existente. La idea es que
cada pregunta mida si se entendió el material y que no se pueda acertar por descarte, por el largo de las
opciones o por el orden en que aparecen.

## De dónde sale cada pregunta

- **Todo sale del material que se sube al repo o se comparte para armar el banco**: los PDFs de teoría,
  los cuestionarios de la cátedra y los parciales anteriores. El enunciado, la respuesta correcta, los
  distractores y la explicación tienen que poder rastrearse a ese material. No se agregan contenidos de
  conocimiento general ni de otras fuentes.
- Si la respuesta no está confirmada (la cátedra no la publica, el archivo la marca como incorrecta sin
  corregirla o la anotación es ambigua), se deduce del apunte y se avisa con `note`, que aparece al
  corregir. Si el material no alcanza para decidir, `correct: []` y la pregunta no se corrige.
- Cuando el PDF está en el repo, la pregunta lleva `source` con la página donde está la respuesta (ver
  [Referencias a la teoría](README.md#referencias-a-la-teoría)).
- En `about` se nombra de dónde sale el banco. Si el material está en Google Drive, se enlaza el archivo:
  quien tiene acceso lo abre, y quien no, ve la pantalla de Google para pedirlo.
- En las preguntas tomadas de parciales reales se respetan el enunciado y la respuesta correcta. Los
  distractores se pueden reescribir para cumplir lo de abajo, siempre con contenido del material.

## Opciones

- **Largo parecido.** La correcta no puede ser sistemáticamente la más larga ni la más detallada.
  Como referencia, en cada pregunta la correcta no debería superar 1,5 veces el largo promedio de los
  distractores, y en todo el banco no debería ser la más larga mucho más seguido que por azar (1 de
  cada 4 preguntas con 4 opciones). Se equilibra alargando los distractores con contenido real o
  acortando la correcta, no agregando relleno.
- **Distractores creíbles.** Definiciones de otros conceptos del mismo apunte, relaciones invertidas
  (causa por efecto, el todo por la parte), órdenes o etapas permutados, clasificaciones de otro autor
  o del tema vecino. Nada absurdo ni obviamente falso.
- **Sin pistas de forma.** Todas las opciones concuerdan en género y número con el enunciado y tienen la
  misma estructura. Los absolutos («siempre», «nunca», «únicamente») no pueden aparecer solo en los
  distractores.
- **Sin referencias al orden.** El motor mezcla las opciones, así que «todas las anteriores» o «ninguna
  de las anteriores» pierden sentido: se escriben como «todas las otras opciones» o «ninguna de las
  otras opciones». Tampoco se usa «la opción a», «b y c», etc.
- **Orden en el JSON.** Aunque el motor las mezcle, se puede apagar «Mezclar opciones»: la correcta no
  va siempre en la misma posición.
- **Selección múltiple.** El enunciado no dice cuántas opciones son correctas («marcá las cuatro…»),
  porque eso permite adivinar.
- **Relacionar (`match`).** Las filas pueden ir en cualquier orden, porque el motor también las mezcla.
  Las opciones del desplegable, como las de arriba, tienen que tener un largo parecido.

## Explicación (`fb`)

- Justifica la respuesta correcta con el material, citando el concepto o la clasificación del apunte.
- Si un distractor es un error común (por ejemplo, la definición de un concepto vecino), la explicación
  dice por qué no corresponde.

## Verificación

`node scripts/validate.mjs` informa, para cada parcial, en cuántas preguntas de opción simple la correcta
es la opción más larga, comparado con lo esperable por azar. Si da bastante más, avisa con ⚠ y lista las
preguntas donde la correcta es mucho más larga que los distractores. El aviso no hace fallar la
validación, pero hay que revisarlo antes de publicar el banco.
