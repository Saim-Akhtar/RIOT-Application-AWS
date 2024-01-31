<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>RIOT Application AWS</h1>
<h3>◦ ► FIT-IoT testbed, RIOT, AWS cloud, Mosquitto MQTT, NodeRed, Influxdb, Grafana</h3> 
<p align="center">
<img src="https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black" alt="C" />
<img src="https://img.shields.io/badge/JSON-000000.svg?style=for-the-badge&logo=JSON&logoColor=white" alt="JSON" />
</p>
<img src="https://img.shields.io/github/license/Awais-Mughal/FIT-LAB-MQTT-AWSIOT?style=for-the-badge&color=5D6D7E" alt="GitHub license" />
<img src="https://img.shields.io/github/last-commit/Awais-Mughal/FIT-LAB-MQTT-AWSIOT?style=for-the-badge&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/Awais-Mughal/FIT-LAB-MQTT-AWSIOT?style=for-the-badge&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/Awais-Mughal/FIT-LAB-MQTT-AWSIOT?style=for-the-badge&color=5D6D7E" alt="GitHub top language" />
</div>

--

##  Table of Contents
- [ Table of Contents](#-table-of-contents)
- [ Overview](#-overview)
- [ repository Structure](#-repository-structure)
- [ Modules](#modules)
- [ Getting Started](#-getting-started)
    - [ Installation](#-installation)
    - [ Running FIT-LAB-MQTT-AWSIOT](#-running-FIT-LAB-MQTT-AWSIOT)
    - [ Tests](#-tests)
    - [ Dashboard](#-dashboard)



---


##  Overview

 In this project an IoT (Internet of Things) sensor node is developed using the RIOT operating system. The sensor node is designed to collect environmental data, including temperature and pressure, and transmit this data to an MQTT (Message Queuing Telemetry Transport) broker using secure protocols,The sensor node communicates with an MQTT broker, and the Mosquitto broker bridge is configured to connect to AWS IoT. and visualizes the data through Grafana.

![Alt text](/Images/SystemArchitecture.png)

---


##  Repository Structure

```sh
└── FIT-LAB-MQTT-AWSIOT/
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


##  Modules

<details closed><summary>RSMB-Broker</summary>

| File                                                                                                   | Summary       |
| ---                                                                                                    | ---           |
| [config.conf](https://github.com/Awais-Mughal/FIT-LAB-MQTT-AWSIOT/blob/main/RSMB-Broker/config.conf) | ► The config.conf file enables MQTT connections, with debug tracing and specific listeners. It also establishes a connection named "local_to_cloud" between sensor node and Mosquitto Client on A8 node on respective ports.|

</details>

<details closed><summary>RIOT-Sensor-Node</summary>

| File                                                                                                   | Summary       |
| ---                                                                                                    | ---           |
| [main.c](https://github.com/Awais-Mughal/FIT-LAB-MQTT-AWSIOT/blob/main/RIOT-Sensor-Node/main.c)             | ► The C program for the IoT sensor node, named "IoTSensors," includes MQTT-SN communication, LPS331AP sensor readings, and a command-line interface (CLI). It periodically measures temperature and pressure, publishes the data to an MQTT broker, and provides status reports via the CLI. The program creates threads for MQTT communication and the main measurement loop. |
| [Makefile](https://github.com/Awais-Mughal/FIT-LAB-MQTT-AWSIOT/blob/main/RIOT-Sensor-Node/Makefile) | ► The Makefile for the SensorNode application in RIOT OS configures a native board, includes necessary modules for sensor and network functionality, sets up MQTT modules for communication, and defines parameters such as server address, port, and MQTT topics.|

</details>

<details closed><summary>Python-MQTT-Subscriber</summary>

| File                                                                                                         | Summary       |
| ---                                                                                                          | ---           |
| [NodeRed_Flow.json](https://github.com/Awais-Mughal/FIT-LAB-MQTT-AWSIOT/blob/main/Python-MQTT-Subscriber/mqtt_subscriber.json) | ► The python script which acts as a mqtt subscriber. It subscribes to the mqtt topic "local_to_cloud" and then it further connects to the InfluxDB to save the payload data in the database.|

</details>

<details closed><summary>Mosquitto-Client-Bridge</summary>

| File                                                                                                                | Summary       |
| ---                                                                                                                 | ---           |
| [mosquitto.config](https://github.com/Awais-Mughal/FIT-LAB-MQTT-AWSIOT/blob/main/Mosquitto-Client-Bridge/mosquitto.config) | ► The mosquitto client bridge which act as a bridge between rsmb broker and AWS EC2 mosquitto client. |

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

7. Start MQTT Broker
From the A8 shared directory, start the Rsmb broker using config.conf
```sh
cd ~/A8
cd RSMB-Broker
./broker_mqtts config.conf
```
![Alt text](/Images/image2.png)

8. Configure and Start Mosquitto Client Bridge
Kill the ports of any existing running mosquitto client
![Alt text](/Images/image3.png)
Modify mosquitto.config with the IPv6 address of the EC2 instance

![Alt text](/Images/image4.png)

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
iotlab-node --flash ./bin/iotlab-m3/SensorNode.elf -l grenoble,m3,104
```


#### Connect to RIOT Sensor Node
Log into the M3 node
```sh
nc m3-104 20000
```
![Alt text](/Images/image5.png)

###  Dashboard 

1. Create EC2 instance and assign IPv6 subnet to the instance following tutorial : 
https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-ipv6-only-subnets-and-ec2-instances/

2. Login to EC2 instance using SSH and install mosquitto broker:
```sh
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients
sudo apt clean
```
3. Verify if the mosquitto service is running:

```sh
sudo service mosquitto status
```
![Alt text](/Images/image6.png)

4. Install docker engine on EC2 instance following the tutorial: https://docs.docker.com/engine/install/ubuntu/

5. Run the node NodeRed container on EC2 instance:

```sh
docker run -it -p 1880:1880 -v node_red_data:/data --name mynodered nodered/node-red
```
6. Run the node Influxdb container on EC2 instance:

```sh
docker run --detach --name influxdb -p 8086:8086 influxdb:2.2.0
```
7. Run the node Grafana container on EC2 instance:

```sh
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```
8. Allow public access on following ports in network security settings:

```sh
Port 1883 (default port for Mosquitto)
Port 1880 (default port for NodeRed)
Port 8086 (default port for Influxdb)
Port 3000 (default port for Grafana)
```
9. On influxdb, setup an organization name, for this project and create a bucket to collect data.

10. On node red add mqtt in network block and connect it to influx out storage block.

![Alt text](/Images/image7.png)

11. Configure mqqt broker with the ip address and port of mosquitto broker running on EC2 instance.

![Alt text](/Images/image8.png)

![Alt text](/Images/image9.png)

12. Configure Influxdb out storage block with the ip address and port of influxdb service runnning on EC2 instances, and add details of bucket created in step 9.

![Alt text](/Images/image10.png)
![Alt text](/Images/image11.png)

13. On Grafana add influxdb as data sources, and add details for the influxdb bucket created in step 9.

![Alt text](/Images/image12.png)
![Alt text](/Images/image13.png)

14. Copy Query code from the influxdb bucket, and use it in grafana dashboard, to add visualization panel for each variable.
![Alt text](/Images/image14.png)
![Alt text](/Images/image15.png)

15. After repeating the previous step for each variable save the dashboard.
![Alt text](/Images/image16.png)


###  Demo Video

[Demo Video](https://www.youtube.com/watch?v=D-Ow4Ak13AE)


