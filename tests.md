## Pruebas hechas

### Prueba 01
* Conv2D -> 15 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0
* Output: Dense -> softmax

Accuracy : 0.9764
Accuracy test : 0.9031

### Prueba 02
* Conv2D -> 10 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0
* Output: Dense -> softmax

Accuracy : 0.8369
Accuracy test : 0.8248

### Prueba 03
* Conv2D -> 20 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0
* Output: Dense -> softmax

Accuracy : 0.9685
Accuracy test : 0.9369

### Prueba 04
* Conv2D -> 25 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0
* Output: Dense -> softmax

Accuracy : 0.9266
Accuracy test : 0.8945

### Prueba 05
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0
* Output: Dense -> softmax

Accuracy : 0.9682
Accuracy test : 0.9342

### Prueba 05b
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> NO
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0
* Output: Dense -> softmax

Accuracy : 0.8895
Accuracy test : 0.8538
Comments: mucho más lenta

### Prueba 06
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 128,relu, dropout = 0.5
* Output: Dense -> softmax

Accuracy : 0.0570
Accuracy test : 0.0570
Comments: Cae completamente 

### Prueba 07
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 256,relu, dropout = 0.5
* Output: Dense -> softmax

Accuracy : 0.056
Accuracy test : 0.0582
Comments: Que ondaaaa

### Prueba 08
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 256,relu, dropout = 0
* Hidden 2: Dense -> 256,relu, dropout = 0.5
* Output: Dense -> softmax

Accuracy : 0.9249
Accuracy test : 0.9131
Comments: 

### Prueba 08
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 256,relu, dropout = 0.5
* Hidden 2: Dense -> 256,relu, dropout = 0.4
* Output: Dense -> softmax

Accuracy : 0.5765
Accuracy test : 0.7311
Comments: 

### Prueba 08 bis
* Conv2D -> 30 (3,3) relu
* Maxpooling2D-> (2,2)
* Flatten
* Hidden 1: Dense -> 256,relu, dropout = 0.5
* Hidden 2: Dense -> 256,relu, dropout = 0.4
* Output: Dense -> softmax

Accuracy : 0.0576
Accuracy test : 0.7311
Comments: ¿Por qué cae tanto si repito el modelo?