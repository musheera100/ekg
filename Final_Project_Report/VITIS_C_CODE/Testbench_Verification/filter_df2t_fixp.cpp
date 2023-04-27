#include "filter_df2t_fixp.h"
typedef ap_fixed<32,16> data_t;
typedef ap_fixed<32,16> y_i_t;
typedef ap_fixed<32,16> x_i_t;
typedef ap_fixed<32,16> temp_t;
typedef ap_fixed<40,8> a_t;
typedef ap_fixed<40,8> b_t;

using namespace std;

void filter_df2t_fixp (hls::stream<AXI_VAL>& y, hls::stream<AXI_VAL>& x) {
	#pragma HLS INTERFACE axis register both port=x
	#pragma HLS INTERFACE axis register both port=y
	#pragma HLS INTERFACE ap_ctrl_none port=return

	while(1) {
		//Values from MATLAB
		//0.049535223542141   0.297211341252848   0.743028353132119   0.990704470842826   0.743028353132119   0.297211341252848   0.049535223542141
		//1.000000000000000  -5.271918566723349  11.619927717930022 -13.702695926669762   9.116066297447906  -3.243419845060293   0.482072025618542

		//coefficients keeping 14 decimal places - gets truncated based on a_t, b_t data types
		b_t b[7] = {0.000000495352235,0.000002972113413,0.000007430283531,0.000009907044708,0.000007430283531,0.000002972113413,0.000000495352235};
		a_t a[7] = {1, -5.271918566723349, 11.619927717930022, -13.702695926669762, 9.116066297447906, -3.243419845060293, 0.482072025618542};
		//b_t b[7] = {0.000000495352235,0x31DD,0x7CA8,0xA636,0x7CA8,0x31DD,0x84F};
		//a_t a[7] = {0x0,0xBA638B78,0x9EB3953A,0x4C1C1EA7,0x1DB68557,0xC1AF3CAE,0x7B691280};
		//b_t b[7] = {b_t(0x000000084F),0x31DD,0x7CA8,0xA636,0x7CA8,0x31DD,0x84F};
		//a_t a[7] = {0x0,0xBA638B78,0x9EB3953A,0x4C1C1EA7,0x1DB68557,0xC1AF3CAE,0x7B691280};

		//0.049535223542141   0.297211341252848   0.743028353132119   0.990704470842826   0.743028353132119   0.297211341252848   0.049535223542141
				//1.000000000000000  -5.271918566723349  11.619927717930022 -13.702695926669762   9.116066297447906  -3.243419845060293   0.482072025618542

				//coefficients keeping 14 decimal places - gets truncated based on a_t, b_t data types
				//b_t b[7] = {0.000000495352235,0.000002972113413,0.000007430283531,0.000009907044708,0.000007430283531,0.000002972113413,0.000000495352235};
				//a_t a[7] = {1, -5.271918566723349, 11.619927717930022, -13.702695926669762, 9.116066297447906, -3.243419845060293, 0.482072025618542};
				//b_t b[7] = {0,0,0,0,0,0,0};
				//a_t a[7] = {1, -5.271918566723349, 11.619927717930022, -13.702695926669762, 9.116066297447906, -3.243419845060293, 0.482072025618542};

				//b_t b[7] = {0x84F,0x31DD,0x7CA8,0xA636,0x7CA8,0x31DD,0x84F};
				//a_t a[7] = {0x0,0xBA638B78,0x9EB3953A,0x4C1C1EA7,0x1DB68557,0xC1AF3CAE,0x7B691280};


				printf("test:\n");
				b_t testy = 1.1;
				int testy2 = 0x1111111111;
				printf("0x%X\n", testy);
				printf("0x%X\n", testy2);

				printf("b:\n");
				printf("0x%X\n", b[0]);
				printf("0x%X\n",b[1]);
				printf("0x%X\n",b[2]);
				printf("0x%X\n",b[3]);
				printf("0x%X\n",b[4]);
				printf("0x%X\n",b[5]);
				printf("0x%X\n",b[6]);

				printf("a:\n");
				printf("0x%X\n",a[0]);
				printf("0x%X\n",a[1]);
				printf("0x%X\n",a[2]);
				printf("0x%X\n",a[3]);
				printf("0x%X\n",a[4]);
				printf("0x%X\n",a[5]);
				printf("0x%X\n",a[6]);


		static data_t shift_reg_v[N];
		x_i_t x_i;
		y_i_t y_i;
		temp_t temp;

		AXI_VAL tmp1;
		x.read(tmp1);


		//Getting current values of x, y
		x_i = x_i_t(tmp1.data);
		y_i = x_i*b[0] + temp;


		int i;
		//Multiply_Accumulate_Loop
		for (i = N - 2; i > 0; i--) {
			shift_reg_v[i] = shift_reg_v[i - 1] + x_i*b[N-i-1] - y_i*a[N-i-1];
		}
		shift_reg_v[0] = x_i*b[N-1] - y_i*a[N-1];

		temp = shift_reg_v[N-2];


		AXI_VAL output;
		output.data = int(y_i);
		output.keep = tmp1.keep;
		output.strb = tmp1.strb;
		output.last = tmp1.last;
		output.dest = tmp1.dest;
		output.id = tmp1.id;
		output.user = tmp1.user;
		y.write(output);


		if (tmp1.last) {
			break;
		}
	}
}






