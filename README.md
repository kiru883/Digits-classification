*LINK - https://simple-mnist-classification.herokuapp.com/

<div align="center">
***Architecture scheme***
</div>
 [![](/static/images/arсhitecture_scheme.png)]

***1. Preprocessing***
- 1.1 Input Preprocessing
 - At the beginning, the message is coming from client side, as message presented in base64 format, it convert in image. It is assumed that the image has a digit so after converting being find bounded digit, this is a rectangle with cutted borders without the parts of digit.
- 1.2 Mnist Preprocessor
 - After then as image has been resized, need transform it in mnist-like image, before the continue we need understand what is mnist image and how it organized?
  ![](/static/images/mnist_ilustrator.png) 
