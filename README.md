# 2024-1 / IIC2173 - E0 | CoolGoat Async

# Dominio
- [numby.me](https://numby.me)
- [www.numby.me](https://www.numby.me)

_"...the Warp Trotter "[Numby](https://honkai-star-rail.fandom.com/wiki/Topaz_and_Numby)," is also capable of acutely perceiving where "riches" are located. It can even perform jobs involving security, debt collection, and actuarial sciences."_

# Consideraciones generales

- El root directory ```/``` redirige automáticamente a ```/fixtures```.
- Se definio el atributo ```flag``` de ```league``` como ```<string|null>``` para ajustrse a los nuevos partidos del ```02/09/2024```.
- El endpoint ```/fixtures{:identifier}``` utiliza el ```id``` del _nested object_ ```fixtures``` para identificar los partidos.
- El parámetro ```page``` en el endpoint ```/fixtures``` comienza desde ```0```.

# Acceso al Servidor

```bash
$ chmod 400 "E0-Arquisis.pem"
$ ssh -i "E0-Arquisis.pem" ubuntu@ec2-34-229-136-170.compute-1.amazonaws.com
```

# Puntos Logrados

## Requisitos Funcionales

- :white_check_mark: **RF1:** Endpoint ```{url}/fixxtures``` mustra los detalles de los partidos recibidos, ordenados por fecha de ultima actualización.
- :white_check_mark: **RF2:** Endpoint ```{url}/fixtures/{id}``` muestra los detalles de un partido en particular.
- :white_check_mark: **RF3:** Se permite paginación y cantidad de partidos por página en el endpoint ```{url}/fixtures```. Para ello se utilizan los parámetros ```page``` y ```count``` respectivamente.
- :white_check_mark: **RF4:** Se permite filtrar los partidos segun los parametros ```home```, ```away``` y ```date``` en el endpoint ```{url}/fixtures```.

## Requisitos No Funcionales

- :white_check_mark: **RNF1:** La conexion al ```broker``` via ```MQTT``` se realiza en un ```container``` independiente. Este realiza un ```post``` a ```/fixtures``` para agregar los partidos a la base de datos.
- :white_check_mark: **RNF2:** Proxy inverso configurado con ```nginx``` directamente en la instancia ```EC2```. La configuración se encuentra en ```/etc/nginx/conf.d/api.conf``` y en ```api.conf``` en el repositorio.
- :white_check_mark: **RNF3:** Dominio obtenido de ```Namecheap```.
- :white_check_mark: **RNF4:** El servidor corre en una instancia ```EC2``` de ```AWS```.
- :white_check_mark: **RNF5:** Se utiliza una base de datos ```PostgreSQL``` en un ```container``` independiente. **Sin bonus de ```Postgis```**.
- :white_check_mark: **RNF6:** La aplicación corre en un ```container``` de ```Docker```.

## Docker Compose

- :white_check_mark: **RNF1:** Se utiliza un archivo ```compose.yaml``` para levantar la aplicación.
- :white_check_mark: **RNF2:** La base de datos se levanta en un ```container``` independiente desde el archivo ```compose.yaml```.
- :white_check_mark: **RNF3:** El _listener_ de ```MQTT``` se levanta en un ```container``` independiente desde el archivo ```compose.yaml```.

## Variable

### HTTPS

- :white_check_mark: **RNF1:** Se utiliza ```certbot``` para obtener un certificado ```SSL``` y habilitar ```HTTPS```.
- :white_check_mark: **RNF2:** Se redirige el tráfico ```HTTP``` a ```HTTPS```.
- :white_check_mark: **RNF3:** Se utiliza el script ```renew.sh``` para renovar el certificado automáticamente en conjunto con ```cron```, ejecutandose cada 12 horas. Los logs se encuentran en ```/var/log/certbot_renew.log```.

### Balanceo de Carga

- :white_check_mark: **RNF1:** Se crean 3 replicas de la aplicación web en el archivo ```compose.yaml```.
- :white_check_mark: **RNF2:** Se utiliza ```nginx``` como _load balancer_ para distribuir el tráfico entre las replicas de la aplicación web.