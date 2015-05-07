/**
 *  bool        Boolean, one byte
 *  byte        Signed byte
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 */

typedef double Label 

struct VSMElement {
	1: i32 feature,
	2: double value
}

typedef list<VSMElement> VSMVector

struct LabelData {
	1: VSMVector data,
	2: Label label 
}

service Classifier {
	Label classify(1:VSMVector data),

	void train(1:list<LabelData> trainingdata)	
}
