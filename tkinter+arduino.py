from pyfirmata import Arduino, util
from tkinter import *
import time

# abrir archivo csv
rp = open("botones.csv", "w+")
# escribir en archivo csv
rp.write("DIRECCIÓN\n")

# Arduino
board = Arduino('/dev/cu.usbmodem14201')

# Botones
button_red = board.get_pin('d:2:i')
button_blue = board.get_pin('d:4:i')
button_white = board.get_pin('d:7:i')
button_yellow = board.get_pin('d:8:i')

# Empezar para empezar a recibir datos del Arduino
it = util.Iterator(board)
it.start()

# Botones
button_red.enable_reporting()
button_blue.enable_reporting()
button_white.enable_reporting()
button_yellow.enable_reporting()

###### Crea pantalla 
root = Tk()
root.minsize(200,30)
root.title("BOTONES")

# Función al apretar exit 
def onExitButtonPress():
    flag.set(False)

# Función al apretar start
def onStartButtonPress():
    while True:
        # Pantalla creada
        if flag.get():
            if str(button_red.read()) == 'True':
                myLabel2.config(text = "Rojo (Izquierda)")
                #print ("rojo")
                rp.write("Izquierda (Rojo)\n")
                
            board.pass_time(0.1)
            if str(button_blue.read()) == 'True':
                myLabel2.config(text = "Azul (Arriba)")
                # print ("azul")
                rp.write("Arriba (Azul)\n")
                
            board.pass_time(0.1)
            if str(button_white.read()) == 'True':
                myLabel2.config(text = "Blanco (Abajo)")
                #print ("blanco")
                rp.write("Abajo (Blanco)\n")
                
            board.pass_time(0.1)
            if str(button_yellow.read()) == 'True':
                myLabel2.config(text = "Amarillo (Derecha)")
                #print ("amarillo")
                rp.write("Derecha (Amarillo)\n")
                
            board.pass_time(0.1)
            root.update()
            time.sleep(0.1)
            startButton.config(state=DISABLED)
        else:
            print("EXIT.")
            break
    board.exit()
    root.destroy()

# Etiquetas
myLabel1 = Label(root, text = "Lectura del circuito")
myLabel1.grid(row=0,column=0)

myLabel2 = Label(root, text= "Bienvenido!")
myLabel2.grid(row=1,column=0)
######

# Al ser creada la pantalla, flag = True
flag = BooleanVar(root)
flag.set(True)

# Boton start en pantalla
startButton = Button(root, text="Comenzar", command=onStartButtonPress)
startButton.grid(column=1, row=3)

# Boton exit en pantalla
exitButton = Button(root, text="Exit", command= onExitButtonPress)
exitButton.grid(column=2,row=3)

# Actualiza pantalla
root.mainloop()
#######


