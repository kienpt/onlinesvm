# onlinesvm
The original version is: http://leon.bottou.org/projects/lasvm
There are couple of modifications:
 - This version runs in online mode. That means you could train incrementally and run test in between different training batches.
 - The code uses Thrift 
 
How to build:
 - First you need to install Thrift: https://thrift.apache.org/

	$./gen.sh

	$make
