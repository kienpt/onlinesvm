import org.apache.thrift.TException;
import org.apache.thrift.transport.TSSLTransportFactory;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TSSLTransportFactory.TSSLTransportParameters;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.io.File;
import java.io.FileReader;
import java.util.List;
import java.util.ArrayList;

/*
*@author: Kien Pham (kien.pham@nyu.edu or kienpt.vie@gmail.com)
*/

public class Client {
  TTransport transport;
  TProtocol protocol;
  Classifier.Client client;

  public Client(String host, int port) {
    try {
      transport = new TSocket(host, port);
      transport.open();

      protocol = new  TBinaryProtocol(transport);
      client = new Classifier.Client(protocol);

    } catch (TException x) {
      x.printStackTrace();
    } 
  }

  public void closeConnection() {
    transport.close();
  }

  private List<LabelData> load_data(String trainfile) {
    List<LabelData> trndata = new ArrayList<LabelData>();
    try{
      File file = new File(trainfile);
      FileReader fileReader = new FileReader(file);
      BufferedReader bufferedReader = new BufferedReader(fileReader);
      String line;
      while ((line = bufferedReader.readLine()) != null) {
        String[] items = line.split(" ");  
        double label = Double.parseDouble(items[0]);
        List<VSMElement> vsm = new ArrayList<VSMElement>();
        for (int i=1; i<items.length; i++) {
          String[] parts = items[i].split(":");
          VSMElement e = new VSMElement();
          e.feature = Integer.parseInt(parts[0]);
          e.value = Float.parseFloat(parts[1]);
          vsm.add(e);
        }
        LabelData ld = new LabelData();
        ld.data = vsm;
        ld.label = label;
        trndata.add(ld);
      }
      fileReader.close();
      return trndata;
    }
    catch(Exception e){
      e.printStackTrace();
      return null;
    }
  }

  public void train(String trainfile) throws TException
  {
    //Train all data at once

    try {
      List<LabelData> data = load_data(trainfile);
      client.train(data);
    } catch (TException x) {
      x.printStackTrace();
    }
  }

  public void train_online(String trainfile) throws TException
  {
    //Test online training: split data into two parts, then train one by one

    try {
      List<LabelData> data = load_data(trainfile);
      //Split training data into 2 parts:
      List<LabelData> data1 = data.subList(0, data.size()/2);
      List<LabelData> data2 = data.subList(data.size()/2, data.size());
      client.train(data1);
      client.train(data2);
    } catch (TException x) {
      x.printStackTrace();
    }
  }

  public void test(String testfile) throws TException
  {
    //Run a test on the trained model
    try {
      List<LabelData> data = load_data(testfile);
      int a = 0;//accuracy
      for (int i=0; i<data.size(); i++) {
        LabelData ld = data.get(i);
        List<VSMElement> vsm = ld.data;
        double label = ld.label;
        double score = client.classify(vsm); 
        if ((label*score) >= 0)
          a += 1;
      }
      System.out.println("Accuracy: " + (double)a/data.size());
    } catch (TException x) {
      x.printStackTrace();
    }
  }

  public void save_model(String model_file)
  {
    //save trained model to file
    try {
      client.save(model_file);
    } catch (TException x) {
      x.printStackTrace();
    }
  }

  public void load_model(String model_file)
  {
    //load saved model from file
    try {
      client.load(model_file);
    } catch (TException x) {
      x.printStackTrace();
    }
  }

  public static void main(String [] args) {
    Client client = new Client("localhost", 9092);
    if (args.length != 2) {
      System.out.println("Wrong argument");
      System.out.println("arguments: [option(-t, -c, -o)] [training_file]");
    }
    String option = args[0];
    String inputfile = args[1];
    try {
      switch (option) {
        case "-t":
          client.train(inputfile);
          break;
        case "-c":
          client.test(inputfile);
          break;
        case "-o":
          client.train_online(inputfile);
          break;
        case "-s":
         client.save_model(inputfile);
         break;
        case "-l":
         client.load_model(inputfile);
         break;
     }
    }
    catch (TException x) {
      x.printStackTrace();
    }
    client.closeConnection();
  }
}
