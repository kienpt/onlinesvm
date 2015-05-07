CXX=g++
THRIFT_VER =thrift
USR_DIR    =/usr/local
THRIFT_DIR =${USR_DIR}/${THRIFT_VER}
INCS_DIRS  =-I${USR_DIR}/include -I${THRIFT_DIR}/include/thrift
LIBS_DIRS  =-L${USR_DIR}/lib -L${USR_DIR}/${THRIFT_VER}/lib
CPP_DEFS   =-D=HAVE_CONFIG_H
CPP_OPTS   =-Wall -O1
LIBS       =-lthrift


TOOLS	= lasvm/vector.c \
		  lasvm/messages.c \
		  lasvm/kernel.c \
		  lasvm/kcache.c \
		  lasvm/lasvm.c

TOOLSINCL= lasvm/vector.h \
		   lasvm/messages.h \
		   lasvm/kernel.h \
           lasvm/kcache.h \
           lasvm/lasvm.h

LASVMSRC=  lasvm/la_online.cpp

LASVM_INC = -Ilasvm

GEN_SRC    = gen-cpp/classification_types.cpp \
             gen-cpp/Classifier.cpp
GEN_INC    = -Igen-cpp



default: server client

server: Server.cpp  $(LASVMSRC) $(TOOLS) $(TOOLSINCL)
	$(CXX) ${CPP_OPTS} ${CPP_DEFS} -o Server ${GEN_INC} ${INCS_DIRS} Server.cpp ${GEN_SRC} ${LIBS_DIRS} ${LASVM_INC} $(LASVMSRC) $(TOOLS) ${LIBS}

client: Client.cpp
	$(CXX) ${CPP_OPTS} ${CPP_DEFS} -o Client ${GEN_INC} ${INCS_DIRS} Client.cpp ${GEN_SRC} ${LIBS_DIRS} ${LIBS}

clean:
	$(RM) -r Client Server
	rm 2>/dev/null la_svm 


#CXX= g++
#CFLAGS= -O3 -Wall
#TOOLS= vector.c messages.c kernel.c kcache.c lasvm.c
#TOOLSINCL= vector.h messages.h kernel.h kcache.h lasvm.h
#LASVMSRC= la_svm.cpp
#LATESTSRC= la_test.cpp
#LSVM2BINSRC= libsvm2bin.cpp
#BIN2LSVMSRC= bin2libsvm.cpp
#
#all: la_svm la_test libsvm2bin bin2libsvm
#
#la_svm: $(LASVMSRC) $(TOOLS) $(TOOLSINCL)
#	$(CXX) $(CFLAGS) -o la_svm $(LASVMSRC) $(TOOLS)  -lm
#
#la_test: $(LATESTSRC) $(TOOLS) $(TOOLSINCL)
#	$(CXX) $(CFLAGS) -o la_test $(LATESTSRC) $(TOOLS)  -lm
#
#libsvm2bin: $(LSVM2BINSRC) $(TOOLS) $(TOOLSINCL)
#	$(CXX) $(CFLAGS) -o libsvm2bin $(LSVM2BINSRC) $(TOOLS) -lm
#
#bin2libsvm: $(BIN2LSVMSRC) $(TOOLS) $(TOOLSINCL)
#	$(CXX) $(CFLAGS) -o bin2libsvm $(BIN2LSVMSRC) $(TOOLS) -lm
#
#clean: FORCE
#	rm 2>/dev/null la_svm la_test libsvm2bin bin2libsvm
#
#FORCE:

