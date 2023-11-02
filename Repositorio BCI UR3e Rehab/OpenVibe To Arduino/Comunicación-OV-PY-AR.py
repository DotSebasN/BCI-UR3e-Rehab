import socket
import serial
import datetime
import csv
from contextlib import closing
from time import sleep


# Configure the serial port parameters
serial_port = 'COM3'  # Replace 'COMx' with the correct serial port name of your Arduino
baud_rate = 57600

# Create a TCP/IP sockets
ClientSocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ClientSocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect the socket to the server's IP address and port
Server_Adress_1 = ('localhost', 5679)
ClientSocket1.connect(Server_Adress_1)

Server_Adress_2 = ('localhost', 5678)
ClientSocket2.connect(Server_Adress_2)

try:
    print("Connected to OpenViBE")

    # Open the serial port connection to Arduino using the contextlib.closing context manager
    with closing(serial.Serial(serial_port, baud_rate)) as arduino:
        i=0
        c10=0 #Reader Arm_M
        c20=0 #Reader Rot_C
        c11=0 #Acc+ Arm_Movement
        c22=0 #Acc+ Rotation_Clockwise
        while i<16:
            # Receive data from OpenViBE (as bytes)
            c1=0
            c2=0
            t=0
            data_bytes = ClientSocket1.recv(3072)
            data_a= ClientSocket2.recv(3072)
            print(f"Received data Stimulation: {data_a}")

            if data_a == b'OVTK_GDF_Arm_Movement\r\n':
                 c10=c10+1
            elif data_a == b'OVTK_GDF_Rotation_Clockwise\r\n':
                 c20=c20+1

            if data_bytes:



                while t<105:
                    data_bytes = ClientSocket1.recv(3072)
                    print(f"Received data: {data_bytes}")

                    if data_bytes == b'OVTK_GDF_Arm_Movement\r\n':
                            c1=c1+1
                            t=t+1
                            sleep(0.0001)

                    elif data_bytes == b'OVTK_GDF_Rotation_Clockwise\r\n':
                            c2=c2+1
                            t=t+1
                            sleep(0.0001) 
                    
                    print(f"C1: {c1} C2: {c2} T: {t}")

                if c1<c2 and data_a == b'OVTK_GDF_Rotation_Clockwise\r\n': 
                    binary_data=b'1'
                    arduino.write(binary_data)
                    c22=c22+1
                    print(f"Data Send: {binary_data}") 
                    sleep(8)
                elif c2<c1 and data_a == b'OVTK_GDF_Arm_Movement\r\n':
                    binary_data=b'0'
                    arduino.write(binary_data)
                    c11=c11+1
                    print(f"Data Send: {binary_data}") 
                    sleep(8)
                else:
                    binary_data=b'3'
                    arduino.write(binary_data)
                    print(f"Data Send: {binary_data}") 
                    sleep(8)
            i=i+1
        Resultados=[
             ['Resultados del Experimento (Agregar Nombre o Marca)'],
             ['Estimulos Generados:    ',(c10+c20)],
             ['Adelante - Atras:       ',c10],
             ['Pronacion - Supinacion: ',c20],
             [''],
             ['Estimulo                ','Aciertos','Clasificacion'],
             ['Adelante - Atras:       ',c11,((c11*100)/c10)],
             ['Pronacion - Supinacion: ',c22,((c22*100)/c20)],
             ['Clasificacion de la Prueba: ',(((c11+c22)*100)/(c10+c20))]
            ]
        with open('Adquisición '+datetime.date.today().strftime("%y_%m_%d")+datetime.datetime.now()+'.csv','w',newline='')as file:
             writer=csv.writer(file, delimiter=' ')
             writer.writerows(Resultados)
                     

                
                

                
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the connection and clean up resources
    ClientSocket1.close()
