#include <stdio.h>
#include <math.h>
#include "filter_df2t.h"
#include <string>
#include <iostream>
#include <fstream>

typedef ap_int<64> int64;

using namespace std;

int main () {
	const int    SAMPLES=100; //15000
	ifstream fin("ECG_good.csv");
	ofstream fout("ECG_out.csv");
	//data_t signal, output;
	//coef_t b[N] = {0.0495*1.0e-05, 0.2972*1.0e-05, 0.7430*1.0e-05, 0.9907*1.0e-05, 0.7430*1.0e-05, 0.2972*1.0e-05, 0.0495*1.0e-05};
	//coef_t a[N] = {1.0000, -5.2719, 11.6199, -13.7027, 9.1161, -3.2434, 0.4821};
	string x_s;
	hls::stream<AXI_VAL> x ("input_stream");
	hls::stream<AXI_VAL> y ("output_stream");
	AXI_VAL data_x;


	for (int i = 0; i<SAMPLES; i++)
	{
		getline(fin, x_s, ',');
		data_x.data = int64(stod(x_s)*1000*1000);


		cout << "Input" << int64(stod(x_s)*1000*1000) << endl;

		data_x.keep=1;
		if(i<(SAMPLES-1))
		{
		  data_x.last=0;
		}
		else
		{
		  data_x.last=1;
		}
		x.write(data_x);
	}

	filter_df2t(y, x);


	for (int i = 0; i<SAMPLES; i++)
	{
		AXI_VAL tmp1;
		y.read(tmp1);
		fout<<tmp1.data.to_double()<<",";
		cout<< "output" << tmp1.data.to_int64() << endl;
	}



  fin.close();
  fout.close();
  if (system("diff -w ECG_out.csv ECG_out_gold.csv")) { //"diff -w ECG_out.csv ECG_out_gold.csv"

	fprintf(stdout, "*******************************************\n");
	fprintf(stdout, "FAIL: Output DOES NOT match the golden output\n");
	fprintf(stdout, "*******************************************\n");
     return 0;
  } else {
	fprintf(stdout, "*******************************************\n");
	fprintf(stdout, "PASS: The output matches the golden output!\n");
	fprintf(stdout, "*******************************************\n");
	return 0;
  }
}
