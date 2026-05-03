# - Visualizador de zonas de cobertura en zonas accidentadas

**Problemática:** al instalar antenas de radioenlace en zonas accidentadas, se necesita saber qué cobertura tendrá la antena considerando:
- altura de la antena y del equipo receptor
- zona de Fresnel
- distancia entre antena y receptor

**Alcance:** simplificar el trabajo del analista de cobertura de radioenlaces.

![](imagenes/resultado_1.png)


# use env

encrypt
```sh
sops encrypt --age PUBLIC_KEY .env > enc.env
```

decrypt
```sh
SOPS_AGE_KEY_FILE=../key.txt sops decrypt enc.env > .env
```