#include <math.h>
#include "filter_df2t_fixp.h"
#include <fstream>

using namespace std;

int main () {
	const int    SAMPLES=15000; //15000
	ifstream fin("ECG_good.csv");
	ofstream fout("ECG_out.csv");
	string x_s;

	hls::stream<AXI_VAL> x ("input_stream");
	hls::stream<AXI_VAL> y ("output_stream");
	AXI_VAL data_x;


	for (int i = 0; i<SAMPLES; i++)
	{
		getline(fin, x_s, ',');
		data_x.data = int(stod(x_s)*1000); // Reading in ECG Data

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

	filter_df2t_fixp(y, x); // Filtering ECG Data


	for (int i = 0; i<SAMPLES; i++)
	{
		AXI_VAL tmp1;
		y.read(tmp1);
		fout<<(tmp1.data.to_double()/1000)<<","; // Writing Result back to file
	}


  fin.close();
  fout.close();

  // Comparing the result to the golden output generated with MATLAB
  ifstream fpga_out("ECG_out.csv");
  ifstream gold_out("ECG_out_gold.csv");
  string fpga_out_s;
  string gold_out_s;

  bool success = 1;
  cout << "test1";
  for (int i = 0; i<SAMPLES; i++)
  {
	  getline(fpga_out, fpga_out_s, ',');
	  getline(gold_out, gold_out_s, ',');

	  // Makes sure that the output of the FPGA is within 5mV of the expected output
	  if(abs(int(stod(fpga_out_s)*1000) - int(stod(gold_out_s)*1000)) > 5)
	  {
		  success = 0;
	  }
  }

  if(success) {
	fprintf(stdout, "*******************************************\n");
	fprintf(stdout, "PASS: The output matches the golden output!\n");
	fprintf(stdout, "*******************************************\n");
	return 0;
  }
  else {
	fprintf(stdout, "*******************************************\n");
	fprintf(stdout, "FAIL: Output DOES NOT match the golden output\n");
	fprintf(stdout, "*******************************************\n");
	return 0;
  }

}
