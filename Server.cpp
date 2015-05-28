#include <thrift/concurrency/ThreadManager.h>
#include <thrift/concurrency/PosixThreadFactory.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/server/TThreadPoolServer.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TTransportUtils.h>
#include <thrift/TToString.h>

#include <iostream>
#include <stdexcept>
#include <sstream>

#include "gen-cpp/Classifier.h"
#include "lasvm/la_online.h"

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::concurrency;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace apache::thrift::server;


/*
* A thrift server that wraps up LASVM
* @author: Kien Pham (kien.pham@nyu.edu or kienpt.vie@gmail.com)
*/

class ClassifierHandler : virtual public ClassifierIf {
 public:
  ClassifierHandler() {
    //default
    cout<<"Parameters are required!!!"<<endl;
  }

  ClassifierHandler(int argc, char **argv) {
    parse_and_initialize(argc, argv);//intialize all parameters after parsing
  }

  void parse_and_initialize(int argc, char **argv) {
     this->initialize_online_model(argc, argv);
     /*
     for(int i=1; i<argc; i++)
     {
       if(argv[i][0] != '-') break;
       ++i;
       switch(argv[i-1][1])
       {
       case 'W':
         this->initialize_without_model(argc, argv);
	     break;
       case 'M':
         this->initialize_fixed_model(argc, argv);
         break;
       case 'O':
         this->initialize_online_model(argc, argv);
         break;
       }
     }
     */
  }
  

  void initialize_without_model(int argc, char **argv) {
	//Initialize without a model
    cout<<"Start server without a model"<<endl;
    online::parse_command_line(argc, argv);
  }

  void initialize_online_model(int argc, char **argv) {
    //Initialize with a model and this model will be updated when `train` is called
    ////Initialize with a fixed model
    cout<<"Start server with online model"<<endl;
    online::parse_command_line(argc, argv);
  }

  Label classify(const VSMVector& data) {
    //Convert VSMVector to lasvm_sparsevector_t
    lasvm_sparsevector_t* sv = lasvm_sparsevector_create();
    for(int i=0; i<data.size(); i++) {
      VSMElement e = data[i];
      lasvm_sparsevector_set(sv,e.feature,e.value);
    }

    double x_sq = lasvm_sparsevector_dot_product(sv, sv);//only RBF kernel requires this
    
	//Classify
	double y=-online::b0;//result
    for(int i=0;i<online::msv;i++)//msv is number of support vectors
    {
      y+=online::alpha_sv[i]*online::kernel(i,x_sq,sv,NULL);
    }
    cout<<"Result: "<<y<<endl;
    return y;
  }

  void train(const std::vector<LabelData> & trainingdata) {
    printf("Train...\n");
    online::libsvm_load_data(trainingdata);
    online::train_online();
    //online::libsvm_save_model();
  }

};

int main(int argc, char **argv) {
  int port = 9092;
  boost::shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());
  boost::shared_ptr<ClassifierHandler> handler(new ClassifierHandler(argc, argv));
  boost::shared_ptr<TProcessor> processor(new ClassifierProcessor(handler));
  boost::shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  boost::shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);

  cout << "Starting the server at " <<port<<"..."<< endl;
  server.serve();
  return 0;
}
