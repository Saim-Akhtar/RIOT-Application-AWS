# RIOT Application AWS


---


##  Overview

 
 
In this project, we have created an IoT (Internet of Things) sensor node utilizing the RIOT operating system. This sensor node is specifically engineered for the collection of environmental data, such as temperature and pressure. The collected data is then securely transmitted to an MQTT (Message Queuing Telemetry Transport) broker through secure protocols. The sensor node establishes communication with an RSMB broker, and the configuration of the Mosquitto client bridge enables a connection to AWS EC2. Subsequently, a Python MQTT client subscribed to the topic stores the data in InfluxDB, and the information is visualized through Grafana.

![Alt text](/Images/SystemArchitecture.png)

---


##  Directory Structure

```sh
└── RIOT-Application-AWS/
    ├── RSMB-broker/
    │   └── config.conf
    ├── Python-MQTT-subscriber/
    │   └── mqtt_subscriber.py
    ├── Mosquitto-Client-Bridge/
    │   └── mosquitto.config
    └── RIOT-Sensor-Node/
        ├── Makefile
        └── main.c

```

---


##  Files and Folders

<details closed><summary>RSMB-Broker</summary>

| File                                                                                                   | Summary       |
| ---                                                                                                    | ---           |
| [config.conf](https://github.com/Saim-Akhtar/RIOT-Application-AWS/blob/main/RSMB-Broker/config.conf) | ► The config.conf file enables MQTT connections, with debug tracing and specific listeners. It also establishes a connection named "local_to_cloud" between sensor node and Mosquitto Client on A8 node on respective ports.|

</details>

<details closed><summary>RIOT-Sensor-Node</summary>

| File                                                                                                   | Summary       |
| ---                                                                                                    | ---           |
| [main.c](https://github.com/Saim-Akhtar/RIOT-Application-AWS/blob/main/RIOT-Sensor-Node/main.c)             | ► The C program for the IoT sensor node, named "IoTSensors," includes MQTT-SN communication, LPS331AP sensor readings, and a command-line interface (CLI). It periodically measures temperature and pressure, publishes the data to an MQTT broker, and provides status reports via the CLI. The program creates threads for MQTT communication and the main measurement loop. |
| [Makefile](https://github.com/Saim-Akhtar/RIOT-Application-AWS/blob/main/RIOT-Sensor-Node/Makefile) | ► The Makefile for the IoTSensors application in RIOT OS configures a native board, includes necessary modules for sensor and network functionality, sets up MQTT modules for communication, and defines parameters such as server address, port, and MQTT topics.|

</details>

<details closed><summary>Python-MQTT-Subscriber</summary>

| File                                                                                                         | Summary       |
| ---                                                                                                          | ---           |
| [NodeRed_Flow.json](https://github.com/Saim-Akhtar/RIOT-Application-AWS/blob/main/Python-MQTT-Subscriber/mqtt_subscriber.json) | ► The python script which acts as a mqtt subscriber. It subscribes to the mqtt topic "local_to_cloud" and then it further connects to the InfluxDB to save the payload data in the database.|

</details>

<details closed><summary>Mosquitto-Client-Bridge</summary>

| File                                                                                                                | Summary       |
| ---                                                                                                                 | ---           |
| [mosquitto.config](https://github.com/Saim-Akhtar/RIOT-Application-AWS/blob/main/Mosquitto-Client-Bridge/mosquitto.config) | ► The mosquitto client bridge which act as a bridge between rsmb broker and AWS EC2 mosquitto client. |

</details>

---

##  Getting Started

###  Installation

1. Clone the RIOT-Application-AWS repository:
```sh
git clone https://github.com/Saim-Akhtar/RIOT-Application-AWS
```

2. Change to the project directory:
```sh
cd RIOT-Application-AWS
```

###  Running RIOT-Application-AWS

1. Connect to Grenoble SSH Frontend
```bash
ssh <login>@grenoble.iot-lab.info
```

2. Start Experiment on IoT-Lab Test Bed

Launch an experiment with two M3 nodes and one A8 node
Wait for the experiment to reach the "Running" state.
I have used 103,104 of M3 nodes and 106 of A8 node as an example. You can use any other node-ids
```sh
iotlab-experiment submit -n iot -d 120 -l grenoble,m3,103-104 -l grenoble,a8,106
```


3. Setup Border Rounter on one of the M3 Nodes
Source RIOT environment
```sh
source /opt/riot.source
```
Build border router firmware for M3 node with baudrate 500000
```sh
make ETHOS_BAUDRATE=500000 DEFAULT_CHANNEL=20 BOARD=iotlab-m3 -C RIOT/examples/gnrc_border_router clean all
```


4. Flash Border Router
Now flash the border router to the first M3 node (m3-1 in this case)
```sh
iotlab-node --flash RIOT/examples/gnrc_border_router/bin/iotlab-m3/gnrc_border_router.elf -l grenoble,m3,103
```


5. Configure Border Router Network
Choose an IPv6 prefix for the grenoble site (e.g., 2001:660:5307:3100::/64 to 2001:660:5307:317f::/64)
Configure the network of the border router on m3-103
Setup a tap interface and an IPv6 prefix with ethos_uhcpd.py
```sh
sudo ethos_uhcpd.py m3-103 tap0 2001:660:5307:3100::1/64
```

6. Setup RSMB Broker and Mosquitto Bridge on A8 Node. 
In a new terminal connect to the SSH frontend, and login into clone the mqtt_broker and mosquitto bridge configuration files in A8 shared directory.
SSH into the A8 node
```sh
ssh root@node-a8-106
```
Check the global IPv6 address of the A8 node and copy it to use in RIOT Sensor Node
```sh
ifconfig
```

7. Start Rsmb Broker
From the A8 shared directory, start the Rsmb broker using config.conf
```sh
cd ~/A8
cd RSMB-Broker
./broker_mqtts config.conf
```

8. Configure and Start Mosquitto Client Bridge
Kill the ports of any existing running mosquitto client
Check the existing mosquitto ports by the following command

```sh
ps -ef | grep mosquitto
```
If there is a port in use, kill the port by using the following command
```sh
kill <port>
```

9. Modify mosquitto.config with the IPv6 address of the EC2 instance
```sh
#Paste your AWS Mosquitto MQTT address in the form of <IPv6 address>:<port>
address <IPv6 address of EC2 instance>:1883

#Example: address 2a05:d016:c59:1d18:70d3:bed4:fc5a:68ac:1883
```

Start Mosquitto service
```sh
root@node-a8-3:~/A8/Mosquitto-Client-Bridge/mqtt_bridge# mosquitto -c mosquitto.conf
```

#### Setup and Build Flash RIOT Sensor Node Firmware
From new terminal connect again to SSH front end of grenoble site and enter the RIOT-Sensor-Node
```sh
cd RIOT-Sensor-Node
```
Build the firmware for the riot sensor node using A8 node's IPv6 address (copied previously) and tap-id (i.e. 0 in our case)
```sh
make DEFAULT_CHANNEL=20 SERVER_ADDR=<IPv6 address> EMCUTE_ID=station0 BOARD=iotlab-m3 -C . clean all
```

#### Flash the riot sensor node firmware on an M3 node 104
```sh
iotlab-node --flash ./bin/iotlab-m3/IoTSensors.elf -l grenoble,m3,104
```


#### Connect to RIOT Sensor Node
Log into the M3 node
```sh
nc m3-104 20000
```

###  AWS Cloud EC2

1. Create EC2 instance and assign IPv6 subnet according to the following tutorial : 
https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-ipv6-only-subnets-and-ec2-instances/

2. Login to EC2 instance using SSH and install mosquitto client using apt-get:
```sh
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
sudo apt clean
```
3. Check if the mosquitto service is running (It should show broker running):

```sh
sudo service mosquitto status
```

4. Allow anonymous connections on mosquitto configurations and enable listener 1883

```sh
sudo nano /etc/mosquitto/mosquitto.conf
```
and then add the follow lines in the file
```bash
listener 1883
allow_anonymous true

```
Then restart the mosquitto service:
```sh
sudo service mosquitto restart
```

5. Install docker on EC2 instance:
```sh
sudo snap install docker
```

6. Setup the Influxdb container on EC2 instance:

```sh
docker run --detach --name influxdb -p 8086:8086 influxdb:2.2.0
```
7. Setup the Grafana container on EC2 instance:

```sh
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```
8. Make sure to have the following ports publicly accessible in security setting of EC2:

![Alt text](/Images/7.jpg)

9. Go to InfluxDB using <EC2-public-IPv4-Address>:8086, setup an organization name and create a bucket.

10. Start running the python mqtt subscriber:

![Alt text](/Images/5.jpg)

11. This is how the data will be visible on InfluxDB:
![Alt text](/Images/1.jpg)

12. On Grafana add influxdb as data sources, and add details for the influxdb bucket which you created in previous steps.

![Alt text](/Images/6.jpg)

13. Copy the Query code from the influxdb bucket:
![Alt text](/Images/2.jpg)

and paste it in grafana dashboard, to just simply view the data in the table.
![Alt text](/Images/4.jpg)



###  Demo Video

[Demo Video](https://www.youtube.com/watch?v=D-Ow4Ak13AE)

