#@author: Kien Pham (kien.pham@nyu.edu)
import sys
sys.path.append('./gen-py')

from classification import Classifier
from classification.ttypes import *
from classification.constants import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol



def load_training_data(training_file):
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
   
    trndata = load_training_data(training_file)
    client.train(trndata)
   
    transport.close()

def train_online(training_file):
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
   
    trndata = load_training_data(training_file)
    middle = len(trndata)/2
    
    trndata1 = trndata[:middle]
    trndata2 = trndata[middle:]
    print "Training first part: "
    client.train(trndata1)
    print "Training second part: "
    client.train(trndata2)
   
    transport.close()


def test(test_file):
    port = 9092
    transport = TSocket.TSocket('localhost', port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Classifier.Client(protocol)
    transport.open()
   
    trndata = load_training_data(test_file) #training and test data have the same format
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


def main(argv):
    option = argv[0]
    input_file = argv[1]
    if option == "-t":#train
        train(input_file)
    elif option == "-c":#classify
        test(input_file)
    elif option == "-o":#online training. Split training data into two pieces and train one by one
        train_online(input_file)


if __name__=="__main__":
    main(sys.argv[1:])    
