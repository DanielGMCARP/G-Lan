# Games-Lan GUI

Interfaz gráfica moderna para la plataforma de juegos Games-Lan, construida con Tkinter.

## 🚀 Características

### ✨ Interfaz Moderna
- **Diseño oscuro** con tema profesional
- **Navegación intuitiva** entre paneles
- **Efectos visuales** y feedback inmediato
- **Responsive** y fácil de usar

### 🎮 Funcionalidades Completas
- **Sistema de autenticación** (login/registro)
- **Catálogo de juegos** con compras
- **Biblioteca personal** con estado de descargas
- **Sistema de descargas** con barra de progreso
- **Procesos en background** (backup, notificaciones)

### 🔄 Concurrencia Avanzada
- **Threads separados** para descargas
- **Procesos background** para tareas pesadas
- **Locks y semáforos** para evitar conflictos
- **UI no bloqueante** durante operaciones

## 📁 Estructura del Proyecto

```
steam_clone_console/
├── src/
│   ├── gui/                    # 🆕 Carpeta de interfaz gráfica
│   │   ├── __init__.py
│   │   ├── main_window.py      # Ventana principal
│   │   ├── login_panel.py      # Panel de login/registro
│   │   ├── menu_panel.py       # Menú principal
│   │   ├── catalog_panel.py    # Catálogo de juegos
│   │   ├── library_panel.py    # Biblioteca personal
│   │   └── download_panel.py   # Panel de descargas
│   ├── gui_app.py             # 🆕 Ejecutable principal GUI
│   ├── main.py                # Versión consola (original)
│   ├── dal.py                 # Acceso a datos
│   ├── db.py                  # Base de datos
│   ├── errores.py             # Manejo de errores
│   ├── gui.py                 # GUI antigua (consola)
│   └── log.py                 # Logging y descargas
└── steam_clone.db             # Base de datos SQLite
```

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.7+
- Tkinter (incluido en Python)
- SQLite3 (incluido en Python)

### Ejecutar la GUI
```bash
cd steam_clone_console/src
python gui_app.py
```

### Ejecutar la versión consola (original)
```bash
cd steam_clone_console/src
python main.py
```

## 🎯 Funcionalidades por Panel

### 🔐 Panel de Login
- **Inicio de sesión** con email y contraseña
- **Registro de nuevos usuarios**
- **Validación de campos** en tiempo real
- **Mensajes de error** claros

### 📋 Menú Principal
- **Navegación rápida** a todas las secciones
- **Información del usuario** actual
- **Botones con efectos hover**
- **Cerrar sesión** seguro

### 📚 Catálogo de Juegos
- **Lista completa** de juegos disponibles
- **Información detallada** (ID, nombre, precio, género)
- **Compra directa** con un clic
- **Actualización en tiempo real**

### 🎮 Biblioteca Personal
- **Juegos comprados** por el usuario
- **Estado de descarga** (pendiente/descargado)
- **Estadísticas** (total y descargados)
- **Colores diferenciados** por estado

### ⬇️ Panel de Descargas
- **Lista de juegos** disponibles para descargar
- **Barra de progreso** visual
- **Porcentaje de descarga** en tiempo real
- **Control de concurrencia** (una descarga a la vez)

## 🔧 Características Técnicas

### Concurrencia
- **Threads**: Descargas en background
- **Procesos**: Backup y notificaciones
- **Locks**: Control de acceso a recursos
- **Queues**: Comunicación entre procesos

### Base de Datos
- **SQLite**: Base de datos local
- **Transacciones**: Operaciones seguras
- **Integridad**: Validación de datos
- **Relaciones**: Usuarios, juegos, biblioteca

### Interfaz de Usuario
- **Tkinter**: Framework nativo de Python
- **Tema oscuro**: Colores profesionales
- **Responsive**: Adaptable a diferentes tamaños
- **Accesible**: Navegación por teclado

## 🎨 Diseño Visual

### Paleta de Colores
- **Fondo principal**: `#2b2b2b` (gris oscuro)
- **Azul primario**: `#4a90e2` (botones principales)
- **Verde éxito**: `#28a745` (acciones positivas)
- **Amarillo advertencia**: `#ffc107` (descargas)
- **Rojo peligro**: `#dc3545` (acciones destructivas)

### Tipografía
- **Títulos**: Arial 18-24pt Bold
- **Texto normal**: Arial 10-12pt
- **Botones**: Arial 10-12pt Bold

## 🚀 Ventajas sobre la Versión Consola

### ✅ Mejoras de Usabilidad
- **Sin superposición** de mensajes
- **Navegación visual** clara
- **Feedback inmediato** para todas las acciones
- **Interfaz intuitiva** para usuarios no técnicos

### ✅ Mejor Concurrencia
- **UI no bloqueante** durante descargas
- **Procesos en background** transparentes
- **Control visual** del progreso
- **Manejo de errores** gráfico

### ✅ Experiencia de Usuario
- **Diseño moderno** y profesional
- **Acceso rápido** a todas las funciones
- **Información visual** clara
- **Interacciones fluidas**

## 🔄 Migración desde Consola

La nueva GUI mantiene **toda la funcionalidad** de la versión consola:

- ✅ Sistema de usuarios (login/registro)
- ✅ Catálogo y compras
- ✅ Biblioteca personal
- ✅ Sistema de descargas
- ✅ Concurrencia (threads, procesos, locks)
- ✅ Base de datos SQLite

## 🎯 Próximas Mejoras

- [ ] **Imágenes de juegos** en el catálogo
- [ ] **Búsqueda y filtros** avanzados
- [ ] **Notificaciones push** del sistema
- [ ] **Temas personalizables** (claro/oscuro)
- [ ] **Atajos de teclado** para power users
- [ ] **Exportar/importar** biblioteca

---

**¡Disfruta de Games-Lan con la nueva interfaz gráfica! 🎮✨** 