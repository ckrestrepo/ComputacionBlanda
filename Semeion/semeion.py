__author__ = 'User'

import numpy  as np
import pylab as plt
w = np.zeros((16,16,10)); L0=5; n=1500; R=10; rho=n/R; R0=10; i=-1
#R radio del mapa
for rec in open('C:\Users\Camilo\Dropbox\UTP-Sistemas\Semestre2-2015\Computacion_Blanda\Semeion\semeion.data'):
    x= np.array(map(float,rec.split())[:256])
    x.resize((16,16))
    plt.imshow(x,cmap = plt.cm.binary, interpolation = 'nearest')
    plt.show()
    #break
    # este break es para el primer registro

    i+=1
    if i > n :break
    x = np.array(map(float,rec.split())[:256])
    x.resize((16,16))
    y = w - np.dstack((x,x,x,x,x,x,x,x,x,x))
    y *= y
    y = np.sum(np.sum(y,axis=0).T,axis=1)
c,v = y.min(),y.argmin()
r = R0*np.exp(-i/rho)
l = l0*np.exp(-i/rho)
for j in range(10):
    phi= np.exp(-((j-v)**2/(2*r*r)))
    w[:,:,j]+=phi*l*(x-w[:,:,j])
for i in range(10):
    plt.subplot(10,1,i+1)
    plt.imshow(w[:,:,i])
plt.show()


