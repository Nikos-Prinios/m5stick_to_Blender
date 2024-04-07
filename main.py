import os, sys, io
import M5
from M5 import *
from hardware import *
from utime import sleep
import network
import socket


connected = 0
sock = None
title0 = None
x = None
y = None
z = None
label1 = None
label2 = None
ax = None
ay = None
az = None


axx = None
ayy = None
azz = None
gxx = None
gyy = None
gzz = None

def linking_blender():
  global sock, connected
  # Établissement de la connexion TCP
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('192.168.1.27', 50000)
  try:
    sock.connect(server_address)
    Speaker.tone(2000, 200)
    connected = 1
  except Exception as e:
    print(f"Echec de la connexion au serveur: {e}")
    sock = None
    connected = 0

def setup():
  global title0, x, y, z, label1, label2, ax, ay, az, axx, ayy, azz, gxx, gyy, gzz, sock

  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect('Lanzarote', 'murielle')
  while not wlan.isconnected():
      pass
  print('Connexion WiFi réussie')

  linking_blender()


  Widgets.fillScreen(0x19293f)
  title0 = Widgets.Title("BLENDER", 7, 0x171212, 0xf57500, Widgets.FONTS.DejaVu18)
  x = Widgets.Label("0.000", 7, 56, 1.0, 0xffffff, 0x19293f, Widgets.FONTS.DejaVu18)
  y = Widgets.Label("0.000", 7, 79, 1.0, 0xffffff, 0x19293f, Widgets.FONTS.DejaVu18)
  z = Widgets.Label("0.000", 7, 102, 1.0, 0xffffff, 0x19293f, Widgets.FONTS.DejaVu18)
  label1 = Widgets.Label(" GYRO : ", 4, 28, 1.0, 0x000000, 0xe3cd11, Widgets.FONTS.DejaVu18)
  label2 = Widgets.Label(" ACCELE :", 5, 132, 1.0, 0x000000, 0xe3cd11, Widgets.FONTS.DejaVu18)
  ax = Widgets.Label("0.000", 7, 162, 1.0, 0xffffff, 0x19293f, Widgets.FONTS.DejaVu18)
  ay = Widgets.Label("0.000", 7, 185, 1.0, 0xffffff, 0x19293f, Widgets.FONTS.DejaVu18)
  az = Widgets.Label("0.000", 7, 208, 1.0, 0xffffff, 0x19293f, Widgets.FONTS.DejaVu18)

  title0.setText('BLENDER')


def loop():
  global title0, x, y, z, label1, label2, ax, ay, az, function, axx, ayy, azz, gxx, gyy, gzz
  M5.update()
  (axx, ayy, azz) = Imu.getAccel()
  ax.setText(str(round(axx,3)))
  ay.setText(str(round(ayy,3)))
  az.setText(str(round(azz,3)))
  (gxx, gyy, gzz) = Imu.getGyro()
  x.setText(str(round(gxx,3)))
  y.setText(str(round(gyy,3)))
  z.setText(str(round(gzz,3)))


  if BtnA.wasSingleClicked():
    if not connected:
      linking_blender()
      print("Trying to reach Blender...")
      Speaker.tone(1000, 100)

  if connected:
    message = f"G,{gxx:.2f},{gyy:.2f},{gzz:.2f};A,{axx:.2f},{ayy:.2f},{azz:.2f}\n"

    try:
      sock.sendall(message.encode())

    except Exception as e:
      print(f"Echec de l'envoi des données: {e}")
  sleep(0.3)


if __name__ == '__main__':
  setup()
  try:
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    sock.close()  # S'assurer de fermer la socket lors de l'arrêt du script
    print("Script terminé proprement.")


    
