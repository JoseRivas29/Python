import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as MessageBox
import serial
from serial.tools import list_ports
import time

conectar = None

def Obterner_Coms():
    puertos_com = [port.device for port in list_ports.comports()]
    return puertos_com

def Actualizar_Coms():
    List_Port['values'] = Obterner_Coms()
    List_Port.set("")

def Connect(port):
    try:
        conectar = serial.Serial(port, baudrate= 9600, stopbits=1, parity= 'N', bytesize=8)
        return conectar
    except serial.SerialException:
        MessageBox.showerror("Error!","Ha ocurrido un error con la comunicacion.")
        return None
    except serial.SerialTimeoutException:
        MessageBox.showerror("Error!","El tiempo de respuesta se paso.")
        return None

def Disconnect(conectar):
    if conectar:
        conectar.close()

def Conectar_Coms():
    global conectar
    if conectar is None:
        port = List_Port.get()
        conectar = Connect(port)
        if conectar:
            btn_connect.config(text="Desconectar")
    else:
        Disconnect(conectar)
        conectar = None
        btn_connect.config(text="Conectar")
        List_Port.set("")

def Enviar():
    try:
        if conectar is None:
             MessageBox.showerror("Error!","Seleccione puerto serial.")
        else:
            data = str(comando.get()) + "\r\n"
            send = data.encode("utf-8")
            print(send)
            conectar.write(send)
    except:
        MessageBox.showerror("Error!","Dato vacio.")



time.sleep(1)

# Configuración de la raíz
root = tk.Tk()
root.title("SendPort")
root.config(bd=15)

comando = tk.IntVar()

ListSerial = tk.Frame(root)
ListSerial.grid(row=0, column=0, columnspan=4)

ttk.Label(ListSerial, text="Selecione el puerto serial", font=("Arial", 12)).pack()

#Lista de puertos com
List_Port = ttk.Combobox(ListSerial, state='readonly')
List_Port.pack(side="left", padx= 5, pady= 5)

#Boton de conectar puerto
btn_connect = tk.Button(ListSerial, text= "Conectar", command= Conectar_Coms)
btn_connect.pack(side="left", padx= 5, pady= 5)

#boton de Actualizar puertos
btn_Actualizar = tk.Button(ListSerial, text= "Actualizar", command= Actualizar_Coms)
btn_Actualizar.pack(side="left", padx= 5, pady= 5)



SenData = tk.Frame(root)
SenData.grid(row=1, column=0, columnspan=4)

ttk.Label(SenData, text="Datos a enviar", font=("Arial", 12)).pack()

Label_Cmmd = tk.Entry(SenData, justify="left", textvariable= comando)
Label_Cmmd.pack(side="left",padx= 5, pady= 5)

btn_Enviar = tk.Button(SenData, text= "Enviar", command= Enviar)
btn_Enviar.pack(side="left",padx= 5, pady= 5)


Actualizar_Coms()

# Finalmente bucle de la apliación
root.mainloop()