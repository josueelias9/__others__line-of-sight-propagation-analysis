# linea-de-vista
daaa no hay nada de documentacion... ahi vamos :D
# avance
## 2022-03-05
despues de una revision rapida, nos damos cuenta que no podremos partir del codigo que ya tenemos. Podremos sacar informacion de el pero no podremos levantar ningun programa.

Desidimos crear nueva carpeta de nombre _proyecto_ y levantamos un VENV para trabajar en el. Detallaremos el proceso. 

```
|-- LINEA-DE-VISTA (repo)
    |-- integral (antiguo)
    |-- proyecto01-05-2019 (antiguo)
    |-- SRTM2029 (antiguo)
    
    |-- flujos.mdj
    |-- README.md
    |-- proyecto (contendra el codigo y el venv)
```
# entorno
- Python 3.8.10
- pip 20.0.2

```bash
cd (ruta hasta LINEA-DE-VISTA)/proyecto
mkdir env
python3 -m venv ./env/
source ./env/bin/activate
```