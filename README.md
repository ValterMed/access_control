## Access Control

Este proyecto de Python está probado con **Python 3.12**.

## Requisitos

- **Python 3.12**
- Se recomienda el uso de [pyenv](https://github.com/pyenv/pyenv) para gestionar la versión de Python.
- Se recomienda utilizar [virtualenv](https://virtualenv.pypa.io/) para crear un entorno virtual.
- Guia práctica para instalación y uso en linux: [Guia Pyen & Virtualenv](https://linux-demon-valter.notion.site/Instalaci-n-Configuraci-n-de-pyenv-y-Pyenv-Virtualenv-3899ab26d80f4edb9d538154f15537ed?pvs=74)

## Instalación y Configuración del Entorno Virtual

Para evitar conflictos con otras dependencias, se recomienda crear un entorno virtual utilizando `pyenv` y `virtualenv`.


### Paso 1: Instalar Python 3.12

Con pyenv, instala Python 3.12 ejecutando:

```bash
pyenv install 3.12.0
```

### Paso 2: Crear un Entorno Virtual

Utiliza pyenv y virtualenv para crear un entorno virtual basado en Python 3.12:

```bash
pyenv virtualenv 3.12.0 access_control_env
```

### Paso 3: Activar el Entorno Virtual

Activa el entorno virtual recién creado:

```bash
pyenv local access_control_env
```

## Instalación de Dependencias

Con el entorno virtual activado, instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## Ejecución del Proyecto

Para ejecutar el proyecto, colócate en la carpeta raíz del proyecto (`access_control`) y ejecuta el siguiente comando:

```bash
python -m app.main
```

## Notas Adicionales

- Asegúrate de tener activado el entorno virtual cada vez que trabajes en el proyecto.
- Si realizas modificaciones en las dependencias, recuerda actualizar el archivo `requirements.txt` o reinstalarlas en el entorno virtual.
- Para cualquier duda o problema, revisa la configuración del entorno virtual y la versión de Python utilizada.
```