# FAST RESTAURANT API - EXCELENTES FUNCIONALIDADES


## Esta es una API hecha con DJANGO, RESTFRAMEWORK, DOCKER, DOCKERCOMPOSE, POSTGRESQL


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



