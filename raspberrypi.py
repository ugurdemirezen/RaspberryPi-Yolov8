import cv2
import io
import socket
import struct
import time
import pickle
import zlib

#İstemci tarafında bir soket oluşturuyoruz ve belirtilen IP adresi ve port numarasına bağlanıyoruz. Bu, sunucu tarafında bekleyen bir bağlantıya katılmak için kullanılır.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.4.4', 8485))
#makefile fonksiyonu, bir soketi dosya nesnesine dönüştürmemize olanak tanır. 'wb' modu, dosyaya yazma ve ikili modu belirtir.
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 640);  # Genişlik: 640 piksel
cam.set(4, 480);  # Yükseklik: 480 piksel
#Bu değişken, gönderilen karelerin sayısını takip etmek için kullanılır.
img_counter = 0
#JPEG formatında sıkıştırma parametreleri belirlenir. Bu parametre, görüntü kalitesini kontrol eder.
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
#cam.read() ile bir kareyi alırız. Ardından, cv2.imencode ile bu kareyi JPEG formatında sıkıştırırız.
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#pickle ile sıkıştırma

    data = pickle.dumps(frame, 0)

#Gönderilecek verinin boyutunu hesaplayarak ekrana yazdırırız.
    size = len(data)

#struct.pack(">L", size) ile paketin boyutunu (byte cinsinden) büyük endian (big-endian) formatında paketleriz. Daha sonra bu boyut bilgisini ve sıkıştırılmış görüntüyü birleştirip sunucuya göndeririz.
    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
#Döngüden çıktıktan sonra, kamerayı serbest bırakarak kullanımını sonlandırırız.
cam.release()