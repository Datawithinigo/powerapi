# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# REFERENCIA PRINCIPAL: 
https://powerapi.org/reference/sensors/hwpc-sensor/#usage
https://powerapi.org/reference/sensors/hwpc-sensor/
https://blog.ptidej.net/using-powerapi-to-measure-the-energy-consumption-of-your-device/

However, 

generaciones 2 a 10
tu 10 = ice lake : 
*  Intel Core Tiger Lake =  11
*  Alder Lake = 12
*  Raptor Lake = 13, 14
c7i 
c7e
c6
c5 (mas consumo / menos rendimiento) + %cpu * tiempo * TDP
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# install docker: 
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker

# parar todo 
docker ps
sudo docker stop $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker system prune -a --volumes

## install the docker elements: 
sudo bash ./smartwatts_install.sh

--> chose all docker options--> easier 

# usamos mongo como base de datos 
sudo docker run -d --name mongo_source -p 27017:27017 mongo


## install influxDB: 
Now that the sensors are writing to MongoDB to store sensor reports, the SmartWatts formula will read from those, and generate new reports to estimate the power consumption of the system. We will write these reports to InfluxDB.

```bash
sudo docker run \
 --name influxdb2 \
 --publish 8086:8086 \
 --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
 --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
 --env DOCKER_INFLUXDB_INIT_MODE=setup \
 --env DOCKER_INFLUXDB_INIT_USERNAME=ADMIN_USERNAME \
 --env DOCKER_INFLUXDB_INIT_PASSWORD=ADMIN_PASSWORD \
 --env DOCKER_INFLUXDB_INIT_ORG=org_test \
 --env DOCKER_INFLUXDB_INIT_BUCKET=power_consumption \
 influxdb:2 

```

http://localhost:8086
ADMIN_USERNAME
ADMIN_PASSWORD

generate all access api token  
* grafana


## grafana: 
sudo docker run -d -p 3000:3000 grafana/grafana

http://localhost:3000

credentials
- admin
- admin

## hostname -I
hostname -I

ip + puerto  local 
http://192.168.1.168:8086


Add header 
Authorization + Token 

database power_consumption

#### heather autentication 
Under Custom HTTP headers, add a new header with the key "Authorization"
"Token <my-token>" 


docker ps -a | grep mongo_destination

perf --> api : 
semana end to end --> version inicial 
manri mentalidad aerea : cambiar rapido cuando no funciona / iterar rapido 







1. Check what's using port 27017:
sudo lsof -i :27017
2. Check all running Docker containers:
docker ps -a


commands to extract mongo infromation: 
sudo lsof -i :27017

docker ps -a

docker rm <container_id>

docker run -d --name mongo_destination -p 27017:27017 mongo

docker exec -it mongo_destination bash


docker exec -it mongo_destination bash

pwd
data/db
ls -la  --> avoid hidden 

find /data -type d | sort

# informations: 
The directories you see are standard MongoDB storage structures:

/data/db - This is the main data directory
/data/db/.mongodb/mongosh - Contains MongoDB shell settings and history
/data/db/diagnostic.data - Stores diagnostic information
/data/db/journal - Contains write-ahead logs for durability


connect mongo shell: 
mongosh
show dbs


use testdb
db.test.insertOne({name: "Test Document", value: 42})
show dbs
db.test.find()



 

ELEMENTS: 
Check if RAPL is supported on your system:
```bash
sudo modprobe intel_rapl_common
ls /sys/class/powercap/intel-rapl
```



bigrobbin@bigrobbin:~/Desktop/PowerAPI/powerapi$ sudo docker exec -it mongo_source mongosh --eval "db.adminCommand('listDatabases')"


in this page : https://blog.ptidej.net/using-powerapi-to-measure-the-energy-consumption-of-your-device/   
how i not  see any  values that i store in mongo db, why i am not storing values?

see all elements : 
