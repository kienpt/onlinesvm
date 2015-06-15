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



default: server cpp java

server: Server.cpp  $(LASVMSRC) $(TOOLS) $(TOOLSINCL)
	$(CXX) ${CPP_OPTS} ${CPP_DEFS} -o Server ${GEN_INC} ${INCS_DIRS} Server.cpp ${GEN_SRC} ${LIBS_DIRS} ${LASVM_INC} $(LASVMSRC) $(TOOLS) ${LIBS}

cpp: Client.cpp
	$(CXX) ${CPP_OPTS} ${CPP_DEFS} -o Client ${GEN_INC} ${INCS_DIRS} Client.cpp ${GEN_SRC} ${LIBS_DIRS} ${LIBS}

JAVA_LIBS=-cp .:java-libs/libthrift-0.9.2.jar:java-libs/slf4j-api-1.7.12.jar:gen-java
java: 
	javac ${JAVA_LIBS} Client.java

clean:
	$(RM) -r Client Server
	rm 2>/dev/null la_svm 
