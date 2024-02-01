# Add the required modules here
USEMODULE += lps331ap
USEMODULE += lsm303dlhc

APPLICATION = IoTSensors

BOARD ?= native

DEVELHELP ?= 1

QUIET ?= 1

RIOTBASE ?= $(CURDIR)/../RIOT

USEMODULE += xtimer

USEMODULE += lps331ap

#Modules for GNRC
USEMODULE += gnrc_netdev_default
USEMODULE += auto_init_gnrc_netif
USEMODULE += gnrc_ipv6_default
USEMODULE += gnrc_icmpv6_error
USEMODULE += gnrc_ipv6_router_default
USEMODULE += gnrc_udp
USEMODULE += gnrc_rpl
USEMODULE += auto_init_gnrc_rpl
USEMODULE += gnrc_pktdump
USEMODULE += gnrc_icmpv6_echo

# Shell modules
USEMODULE += shell
USEMODULE += shell_commands
USEMODULE += ps
USEMODULE += netstats_l2
USEMODULE += netstats_ipv6
USEMODULE += netstats_rpl

#MQTT Modules
USEMODULE += emcute
# SERVER_ADDR ?= 2001:660:5307:3000::67
SERVER_PORT = 1885
# SERVER_PORT = 1883
MQTT_TOPIC_OUT = local_to_cloud
MQTT_TOPIC_IN = cloud_to_local
# EMCUTE_ID = station0

ifneq (,$(EMCUTE_ID))
  CFLAGS += -DEMCUTE_ID=\"$(EMCUTE_ID)\"
endif

#Some flags
CFLAGS += -DSERVER_ADDR='"$(SERVER_ADDR)"'
CFLAGS += -DSERVER_PORT=$(SERVER_PORT)
CFLAGS += -DMQTT_TOPIC_OUT='"$(MQTT_TOPIC_OUT)"'
CFLAGS += -DMQTT_TOPIC_IN='"$(MQTT_TOPIC_IN)"'

include $(RIOTBASE)/Makefile.include
include $(RIOTBASE)/makefiles/default-radio-settings.inc.mk
