# Proyecto de Manipulado Robótico

Este proyecto consiste en un brazo robótico de pequeña escala controlado mediante gestos de la mano. A continuación, encontrarás una descripción detallada del proyecto, sus objetivos, tecnología utilizada y cómo puedes replicarlo.

## Objetivo del Proyecto

El objetivo de este proyecto es poner en práctica y mejorar habilidades en diseño 3D, electrónica y programación. La idea es crear un robot que pueda moverse en respuesta a gestos de la mano reconocidos utiliando la camara de la laptop.

### Componentes Principales

- **Placa de desarrollo ESP32**: Microcontrolador utilizado para controlar los servomotores y recibir por comunicacion serial la posicion de los servo motores.
- **Servomotores**: Motores utilizados para mover las diferentes partes del brazo robótico. Se utilizaron 3 modelos diferentes el MG996R, el MG90S y el SG90; todos de 180 grados.
- **Librería Mediapipe**: Utilizada para el reconocimiento de gestos de la mano. Esta librería cuenta con un modelo de ML ya entrenado que asigna coordenadas a los puntos de la mano y utilizando esto se crean gestos específicos para controlar cada servomotor de forma individual. https://mediapipe-studio.webapps.google.com/studio/demo/hand_landmarker

### Funcionamiento

1. **Reconocimiento de Gestos**: Utilizando Mediapipe, el sistema captura la posición de la mano y asigna coordenadads a puntos clave (landmarks).
2. **Interpretación de Gestos**: En python se interpretan estas coordenadas para identificar gestos específicos y actualizar el angulo del servo en cuestion.
3. **Comunicación con ESP32**: El angulo actualizado se envían al ESP32 a través de comunicación serial.
4. **Control de Servomotores**: El ESP32 recibe los angulos y mueve los servomotores correspondientes.

## Aprendizajes y Descubrimientos

Este proyecto ha sido una excelente oportunidad para mejorar en programación, diseño 3D y electrónica. También ha resaltado la importancia de investigar y aprovechar las herramientas disponibles en internet.

## Próximos Pasos

El objetivo principal es controlar el robot mediante gestos de la mano, pero también estoy trabajando en permitir su control vía web server y con un joystick.


## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes mejoras, sugerencias o encuentras errores no dudes en compartirlas conmigo.

## Datos de contacto

LinkedIn: https://www.linkedin.com/in/felipe-santisteban-facal-1a4452261/

