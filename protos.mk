PROTO_SOURCE_ROOT := $(shell pwd)/protos
PROTO_OUTPUT_PATH := $(shell pwd)/src
PY := $(shell pwd)/.venv/bin/python

INC := -I$(PROTO_SOURCE_ROOT)
PKG := gcp/protobuf
PKG += gcp/rpc
PKG += gcp/api
PKG += gcp/cloud/speech/v2
TARGET_PKG := $(patsubst %,%.pkg,$(PKG))
SRV := gcp/longrunning
SRV += service
TARGET_SRV := $(patsubst %,%.srv,$(SRV))

######################################################################################
# building core

all: clean $(TARGET_PKG) $(TARGET_SRV)
	@printf "make DONE...\r\n"

%.pkg:
	$(PY) -m grpc_tools.protoc $(INC) --python_out=$(PROTO_OUTPUT_PATH) --pyi_out=$(PROTO_OUTPUT_PATH) $(shell find $(PROTO_SOURCE_ROOT)/$(subst .pkg,,$@) -maxdepth 1 -iname "*.proto")

%.srv:
	$(PY) -m grpc_tools.protoc $(INC) --python_out=$(PROTO_OUTPUT_PATH) --pyi_out=$(PROTO_OUTPUT_PATH) --grpc_python_out=$(PROTO_OUTPUT_PATH) $(shell find $(PROTO_SOURCE_ROOT)/$(subst .srv,,$@) -maxdepth 1 -iname "*.proto")

clean:
	@printf "make clean...\r\n"
