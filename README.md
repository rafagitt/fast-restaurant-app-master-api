# FAST RESTAURANT


## Esta es una API hecha con Django, Django Restframework,
## Doker, Docker-compose, conectada a una base de datos Postgresql


#### Características:

PUBLICO: Puede ver la pagina general y los platillos, además de registrarse e iniciar sesion

PRIVADO: Además de lo publico, puede generar pedidos de los platillos de este restaurant, así como cancelarlos

ADMINISTRADOR: Puede Ver, Crear, Actualizar, Eliminar Platillos en su Panel Administrativo, Además debe de estar
pendiente de los pedidos que debe Entregar que le hayan solicitado los clientes,
también puede cancelar los pedidos que le soliciten por teléfono


#### Reglas de la API:

- Para hacer un pedido se debe estar loggeado

- Cada usuario solo puede ver sus propios pedidos con estatus PENDIENTE, CANCELADO y RECIBIDO

- Si un usuario realiza 3 pedidos en un solo día, el ultimo pedido tendrá un fabuloso 50% de descuento

- Si un usuario cancela más de tres veces en un periodo de 4 días no podrá volver
a ordenar platillos en un periodo de 4 días más

- Los Administradores deben poder ver los pedidos de todos, para poder atenderlos o cancelarlos

### Para ejecutar esta aplicacion (Modo Desarrollo) necesita:

###### - Tener Docker instalado

Vaya al directorio que contiene docker-compose.yml y escriba el siguiente comando:

`docker-compose up`

Igual si no esta familiarizado con Docker, tambien puede crear su entorno virtual en python, instalar las dependencias
que vienen en el archivo requirements.txt con PIP y colocar sus variables de entorno en un archivo .env preferentemente
al nivel del mismo documento de texto que contiene dichas dependencias

### Notas a tomar en cuenta para sus pruebas:

Le recomendamos ampliamente para realizar peticiones que requieran token (sobre todo la de logout), utilizar un programa externo
para realizarlas, puede ser POSTMAN o similar o bien conectarla a una interfaz frontend personalizada, para esto ultimo deberá instalar
y agregar Django Cors en el archivo settings.py:

INSTALLED_APPS = ['corsheaders',]

MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',]

CORS_ORIGIN_WHITELIST = ['http://localhost:8000']

---> Django Cors ya vienen incluido en el paquete de dependencia requirements.txt

Ahora bien, supongamos que solo desee probar esta api desde la cómoda interfaz de restframework:

Simplemente en los archivos views.py de app food y app user puede borrar o comentar la linea de código de cada vista que dice:

->  authentication_classes = (TokenAuthentication,)

Inicie Sesión desde Django Admin y listo! Puede probar los diferentes tipos de permisos de casa usuario





