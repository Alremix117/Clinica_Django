# 🏥 Proyecto Clínica — Sistema de Gestión de Pacientes

**Clinica** es una aplicación web desarrollada con **Django 5.2.7**, diseñada para la gestión integral de pacientes, sus datos demográficos, historial médico y vínculos con entidades prestadoras de salud.  
El sistema permite administrar de forma estructurada información sobre diagnósticos, discapacidades, nacionalidad, ocupación y más.

---

## 👥 Desarrollado por

- **Paulina Cartagena González**
- **Andrés Felipe Giraldo Andrade**
- **Fredt Alexander Olivero Zapata**
- **Johan David Peñuela Morales**

---

## ⚙️ Tecnologías principales

| Componente         | Versión | Descripción                                         |
| ------------------ | ------- | --------------------------------------------------- |
| **Python**         | 3.10+   | Lenguaje principal del proyecto                     |
| **Django**         | 5.2.7   | Framework web principal                             |
| **django-jazzmin** | 3.0.1   | Tema visual moderno para el panel de administración |
| **asgiref**        | 3.10.0  | Librería ASGI usada por Django                      |
| **sqlparse**       | 0.5.3   | Utilidad interna de Django para SQL                 |
| **tzdata**         | 2025.2  | Base de datos de zonas horarias                     |

---

## 🚀 Instrucciones para ejecutar el proyecto localmente

Sigue estos pasos para ejecutar el proyecto **Clinica** en un nuevo entorno.

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Alremix117/Clinica_Django.git
cd Clinica
```

---

### 2️⃣ Crear y activar un entorno virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Instalar dependencias

Asegúrate de tener el archivo `requirements.txt` en la raíz del proyecto, luego ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:

```
asgiref==3.10.0
Django==5.2.7
django-jazzmin==3.0.1
sqlparse==0.5.3
tzdata==2025.2
```

---

### 4️⃣ Configurar las variables de entorno (opcional)

Si tu proyecto requiere claves o configuración personalizada, crea un archivo `.env` en la raíz:

```env
DJANGO_SECRET_KEY=tu_clave_secreta
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

> ⚠️ **Importante:** nunca subas tu archivo `.env` a GitHub.

---

### 5️⃣ Aplicar migraciones de base de datos

Ejecuta los siguientes comandos en la raíz del proyecto:

```bash
cd Clinica_Proyecto/
python manage.py makemigrations
python manage.py migrate
```

Esto creará las tablas necesarias en tu base de datos.

---

### 6️⃣ Crear un superusuario (acceso al panel de administración)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para asignar usuario, correo y contraseña.

---

### 7️⃣ Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Luego abre tu navegador en:

```
http://127.0.0.1:8000/
```

---

## 🧰 Comandos útiles de Django

| Acción                        | Comando                            |
| ----------------------------- | ---------------------------------- |
| Crear migraciones             | `python manage.py makemigrations`  |
| Aplicar migraciones           | `python manage.py migrate`         |
| Crear superusuario            | `python manage.py createsuperuser` |
| Ejecutar servidor local       | `python manage.py runserver`       |
| Verificar errores del sistema | `python manage.py check`           |
| Actualizar dependencias       | `pip freeze > requirements.txt`    |

---

## 🎨 Tema de administración (Jazzmin)

Este proyecto incluye la librería **[django-jazzmin](https://github.com/farridav/django-jazzmin)** para mejorar la interfaz del panel de administración.  
Una vez ejecutado el servidor, accede al panel desde:

```
http://127.0.0.1:8000/admin/
```

Y notarás una interfaz moderna y mejorada.

---

## 🧪 Buenas prácticas recomendadas

- Usar **entornos virtuales** (`venv` o `conda`).
- Mantener el archivo `requirements.txt` actualizado.
- No subir archivos sensibles (`.env`, credenciales, backups).
- Hacer commits pequeños y descriptivos.
- Probar los cambios con `python manage.py check` antes de cada commit.

---

## 📄 Licencia

Este proyecto es de uso académico.  
Puedes modificarlo o extenderlo para propósitos educativos o de investigación, dando crédito a los autores originales.

---

## 🌐 Contacto

Si tienes dudas, sugerencias o deseas contribuir al proyecto, puedes abrir un **issue** en el repositorio de GitHub o contactar a cualquiera de los desarrolladores.

---

💙 _Proyecto desarrollado con Django — Tecnológico de Antioquia / Formación Académica._
