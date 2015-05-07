# onlinesvm
The original version is: http://leon.bottou.org/projects/lasvm
There are couple of modifications:
 - This version runs in online mode. That means you could train incrementally and run test in between different training batches.
 - The tool runs as daemon and use Thrift for communication. You could write your own client in different languages to interact with the tool. 
 
How to build:
 - First you need to install Thrift: https://thrift.apache.org/

	$./script/gen.sh

	$make

Run a test:
    
  - Run server wihout finishing step:

	$./Server -o 0

  - Online training:

    $./script/online.sh

  - Test classification

    $./script/test.sh
