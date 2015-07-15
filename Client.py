import sys
sys.path.append('./gen-py')

from classification import Classifier
from classification.ttypes import *
from classification.constants import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


#@author: Kien Pham (kien.pham@nyu.edu or kienpt.vie@gmail.com)

def load_data(training_file):
    trndata = []
    with open(training_file) as lines:
        for line in lines:
            items = line.strip().split()
            label = items[0]
            vsm = []
            for item in items[1:]:
                index, value = item.split(":")
                e = VSMElement()
                e.feature = int(index)
                e.value = float(value)
                vsm.append(e)
            v = LabelData()
            v.data = vsm
            v.label = int(label)
            trndata.append(v)
    return trndata

def train(training_file):
    '''
    Train all data at once
    '''

    port = 9092
    # Make socket
    transport = TSocket.TSocket('localhost', port)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = Classifier.Client(protocol)
    # Connect!
    transport.open()
   
    trndata = load_data(training_file)
    client.train(trndata)
   
    transport.close()

def train_online(training_file):
    '''
    Test online training: split data into two parts, then train one by one
    '''

    port = 9092
    # Make socket
    transport = TSocket.TSocket('localhost', port)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = Classifier.Client(protocol)
    # Connect!
    transport.open()
   
    trndata = load_data(training_file)
    middle = len(trndata)/2
    
    trndata1 = trndata[:middle]
    trndata2 = trndata[middle:]
    print "Training first part: "
    client.train(trndata1)
    print "Training second part: "
    client.train(trndata2)
   
    transport.close()


def test(test_file):
    #Run a test on the trained model
    port = 9092
    transport = TSocket.TSocket('localhost', port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Classifier.Client(protocol)
    transport.open()
   
    trndata = load_data(test_file) #training and test data have the same format
    a = 0
    c = 0
    for data in trndata:
        c+=1
        vsm = data.data
        label = data.label
        res = client.classify(vsm)
        y = "-1"
        if(res>=0):
            y="1"
        print "Label: " + str(label) + ", Result: " + str(res) + ", y: " + y
        if label == int(y):
          a+=1
        #break
    print "accuracy: "  + str(a/float(c))
    transport.close()

def save_model(model_file):
    #Saving the trained model to file.
    #Must run after train()
    port = 9092
    transport = TSocket.TSocket('localhost', port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Classifier.Client(protocol)
    transport.open()   
    client.save(model_file)
    transport.close()

def load_model(model_file):
    #Load the saved model from file.
    port = 9092
    transport = TSocket.TSocket('localhost', port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Classifier.Client(protocol)
    transport.open()   
    client.load(model_file)
    transport.close()

def load_then_train_model(training_file, option):
    model_file = "test_load_and_train.model"
    if (option == "1"): #Train the first half of training data
        port = 9092
        # Make socket
        transport = TSocket.TSocket('localhost', port)
        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # Create a client to use the protocol encoder
        client = Classifier.Client(protocol)
        # Connect!
        transport.open()
   
        trndata = load_data(training_file)
        middle = len(trndata)/2
        
        trndata1 = trndata[:middle]
        print "Training first part: "
        client.train(trndata1)
   
        transport.close()

        save_model(model_file) 
    elif (option == "2"):
        load_model(model_file)    
        port = 9092
        # Make socket
        transport = TSocket.TSocket('localhost', port)
        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # Create a client to use the protocol encoder
        client = Classifier.Client(protocol)
        # Connect!
        transport.open()
   
        trndata = load_data(training_file)
        middle = len(trndata)/2
        
        trndata2 = trndata[middle:]
        print "Training second part: "
        client.train(trndata2)
   
        transport.close()

def main(argv):
    if len(argv) < 2:
        print "Wrong arguments"
        print "arguments: [option(-t, -c, -o)] [training_file|model_file]"
        print "or: -tt [training_file|model_file] [action]"
        return
    option = argv[0]
    _file = argv[1]
    if option == "-t":#train
        train(_file)
    elif option == "-c":#classify
        test(_file)
    elif option == "-o":#online training. Split training data into two pieces and train one by one
        train_online(_file)
    elif option == "-s": #save the current model
        save_model(_file)
    elif option == "-l": #load the saved model
        load_model(_file)
    elif option == "-tt": #test load then train model
        #How to run: 
        #1: $python Client.py -tt training_file 1 
        #2: $python Client.py -tt training_file 2 
        action = argv[2] #action is "1" to train the first part of data. "2" to load model and train the second part
        load_then_train_model(_file, action)


if __name__=="__main__":
    main(sys.argv[1:])    
