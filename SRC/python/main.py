import serial
import cv2
import mediapipe as mp
import time as t

# Inicializacion del puerto serial 
ser = serial.Serial('/dev/cu.usbserial-0001', 115200)

# Inicializacion de variables
angulos_servo = [90, 90, 90, 90, 60] # base, brazo1, brazo2, brazo3, agarre
estado_garra = False  # Estado de la garra: False = abierta (60), True = cerrada (0)
reset_gesto_garra = False

# Inicializacion de los módulos de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_manos = mp.solutions.hands

# Inicializacion de la camara
camara = cv2.VideoCapture(0)

# Funciones de utilidad
def limitar_valor(valor, minimo, maximo):
    return max(min(maximo, valor), minimo)

def estan_cerca(valor1, valor2, tolerancia):
    return abs(valor1 - valor2) < tolerancia

# Bucle principal
with mp_manos.Hands(model_complexity=0, min_detection_confidence=0.6, min_tracking_confidence=0.6) as manos:
    # Tiempos de retraso para que no se actualicen los ángulos de los servos muy rápido
    tiempo_garra = t.time()  # Tiempo para control de la garra

    while camara.isOpened():
        hay_mano, imagen = camara.read()

        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        resultado = manos.process(imagen_rgb)

        if resultado.multi_hand_landmarks:
            for landmarks in resultado.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    imagen, 
                    landmarks, 
                    mp_manos.HAND_CONNECTIONS, 
                    mp_drawing_styles.get_default_hand_landmarks_style(), 
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                muneca_x = 1000 * landmarks.landmark[0].x
                dedo_gordo_x = 1000 * landmarks.landmark[4].x
                dedo_menique_x = 1000 * landmarks.landmark[20].x
                dedo_indice_x = 1000 * landmarks.landmark[8].x
                dedo_medio_x = 1000 * landmarks.landmark[12].x
                dedo_anular_x = 1000 * landmarks.landmark[16].x

                falange_indice_y = 1000 * landmarks.landmark[6].y
                falange_medio_y = 1000 * landmarks.landmark[10].y
                falange_anular_y = 1000 * landmarks.landmark[14].y
                falange_menique_y = 1000 * landmarks.landmark[18].y
                falange_gordo_y = 1000 * landmarks.landmark[2].y

                base_dedo_indice_y = 1000 * landmarks.landmark[5].y
                base_dedo_medio_y = 1000 * landmarks.landmark[9].y
                base_dedo_anular_y = 1000 * landmarks.landmark[13].y
                base_dedo_menique_y = 1000 * landmarks.landmark[17].y

                muneca_y = 1000 * landmarks.landmark[0].y
                dedo_indice_y = 1000 * landmarks.landmark[8].y
                dedo_menique_y = 1000 * landmarks.landmark[20].y
                dedo_medio_y = 1000 * landmarks.landmark[12].y
                dedo_anular_y = 1000 * landmarks.landmark[16].y
                dedo_gordo_y = 1000 * landmarks.landmark[4].y

                # Control del agarre 
                if estan_cerca(dedo_gordo_x, dedo_menique_x, 30) and estan_cerca(dedo_gordo_y, dedo_menique_y, 30) and not estan_cerca(dedo_gordo_y, dedo_indice_y, 100) and not estan_cerca(dedo_menique_y, dedo_anular_y, 100) and t.time() - tiempo_garra > 1 and dedo_medio_y < falange_medio_y and dedo_indice_y < falange_indice_y and dedo_anular_y < falange_anular_y:
                    tiempo_garra = t.time()
                    if(angulos_servo[4] == 60):
                        angulos_servo[4] = 0
                    else:
                        angulos_servo[4] = 60

                # Movimiento articulacion 1
                if dedo_indice_y > falange_indice_y and falange_medio_y > dedo_medio_y and falange_anular_y > dedo_anular_y and falange_menique_y > dedo_menique_y:
                        # Esta apuntando con un dedo para abajo
                        angulos_servo[1] = limitar_valor(angulos_servo[1] - 4, 0, 180)
                elif dedo_indice_y < falange_indice_y and dedo_medio_y > falange_medio_y and dedo_anular_y > falange_anular_y and dedo_menique_y > falange_menique_y:
                        # Esta apuntando con un dedo para arriba
                        angulos_servo[1] = limitar_valor(angulos_servo[1] + 4, 0, 180)
                
                # Movimiento articulacion 2
                if dedo_indice_y < muneca_y and dedo_indice_y < falange_indice_y and dedo_medio_y < muneca_y and dedo_medio_y < falange_medio_y and falange_anular_y < dedo_anular_y and falange_menique_y < dedo_menique_y:
                     # Esta apuntando con dos dedos para arriba
                    angulos_servo[2] = limitar_valor(angulos_servo[2] + 4, 0, 180)
                elif dedo_indice_y > muneca_y and dedo_indice_y > falange_indice_y and dedo_medio_y > falange_medio_y and dedo_anular_y < falange_anular_y and dedo_menique_y < falange_menique_y:
                    angulos_servo[2] = limitar_valor(angulos_servo[2] - 4, 0, 180)
                
                # Movimiento articulacion 3
                if estan_cerca(dedo_gordo_x, dedo_indice_x, 50) and estan_cerca(dedo_indice_x, dedo_medio_x, 50) and estan_cerca(dedo_medio_x, dedo_anular_x, 50) and estan_cerca(dedo_anular_x, dedo_menique_x, 50) and estan_cerca(dedo_gordo_y, dedo_medio_y, 50):
                    if dedo_menique_y < falange_menique_y and dedo_gordo_y < falange_gordo_y:
                        angulos_servo[3] = limitar_valor(angulos_servo[3] + 4, 0, 180)
                    else:
                        angulos_servo[3] = limitar_valor(angulos_servo[3] - 4, 0, 180)
                    
                # Movimiento de la base
                if abs(dedo_anular_x - 50 - muneca_x) > 100 and dedo_anular_y < falange_anular_y and dedo_menique_y < falange_menique_y and dedo_medio_y < falange_medio_y and dedo_indice_y < falange_indice_y:
                    if dedo_anular_x > muneca_x:
                        angulos_servo[0] = limitar_valor(angulos_servo[0] - 4, 0, 180)
                    else:
                        angulos_servo[0] = limitar_valor(angulos_servo[0] + 4, 0, 180)
        

        ser.write(bytearray(angulos_servo))
        print(angulos_servo)

        cv2.putText(imagen, str(angulos_servo), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 100, 0), 2, cv2.LINE_AA)
        cv2.imshow('MediaPipe Hands', imagen)
        

        if cv2.waitKey(5) & 0xFF == 27:
            break

camara.release()
cv2.destroyAllWindows()
