# Alma de Oro

Este es un **proyecto académico universitario** realizado con el fin de aprender a hacer uso de Django y Python como lenguaje de backend aplicado a un caso real.

Este proyecto fue desarrollado con la colaboración de:

* [Mariana González](https://github.com/Mariana44-max)
* [Valentina Ruiz](https://github.com/valentina2209-avr)
* [Esteban Bonilla](https://github.com/estebanbonilla22)
* [Alejandro Ospina](https://github.com/Alejoor18)
* [Santiago Leyton](https://github.com/SantiagoLeyton)

---

## 🛠️ Tecnologías utilizadas


<p align="left">
  <img alt="Python" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50" height="50"/>
  <img alt="JavaScript" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="50" height="50"/>
  <img alt="HTML5" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="50" height="50"/>
  <img alt="CSS3" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="50" height="50"/>
  <img alt="Django" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="50" height="50"/>
  <img alt="Git" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="50" height="50"/>
</p>

---

## 🚀 Cómo poner en marcha el proyecto

Sigue estos pasos para clonar el proyecto y hacer que la API funcione en tu equipo:

### 1. Clonar el repositorio

```powershell
git clone https://github.com/tu-usuario/alma-de-oro.git
cd alma-de-oro
```

### 2. Crear y activar entorno virtual

En **Windows**:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

En **Linux/Mac**:

```powershell
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```powershell
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```powershell
python manage.py runserver
```

La API estará disponible en:
👉 `http://127.0.0.1:8000/`

---

## 🎯 Objetivo del proyecto

Este repositorio busca servir como **guía práctica y académica** para entender cómo estructurar y levantar un backend en Django, integrándolo con tecnologías modernas de frontend.
