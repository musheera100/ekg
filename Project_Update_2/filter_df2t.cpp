#include <stdio.h>
#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include "filter_df2t.h"
typedef ap_axis<64,1,1,1> AXI_VAL;
typedef ap_int<96> data_t;
typedef ap_int<96> y_i_t;
typedef ap_int<96> x_i_t;
typedef ap_int<96> temp_t;
typedef ap_int<64> a_t;
typedef ap_int<64> b_t;

typedef ap_int<96> int96;
typedef ap_int<64> int64;

using namespace std;

//#define N 7

void filter_df2t (hls::stream<AXI_VAL>& y, hls::stream<AXI_VAL>& x) {
	//#pragma HLS INTERFACE m_axi depth=7 port=c
	#pragma HLS INTERFACE axis register both port=x
	#pragma HLS INTERFACE axis register both port=y
	#pragma HLS INTERFACE ap_ctrl_none port=return
	// coef_t taps[N] = {0,-10,-9,23,56,63,56,23,-9,-10,0};


	while(1) {
		b_t b[7] = {17,100,249,332,249,100,17};
		a_t a[7] = {33554432, -176896233, 389900074, -459786179, 305884427, -108831111, 16175653};
		static data_t shift_reg_v[N];
		x_i_t x_i;
		y_i_t y_i;
		temp_t temp;

		AXI_VAL tmp1;
		x.read(tmp1);

		//Getting current values of x, y
		x_i = tmp1.data.to_int64();
		y_i = x_i*b[0] + shift_reg_v[N-2];

		int i;
		Multiply_Accumulate_Loop:
		for (i = N - 2; i > 0; i--) {
			//#pragma HLS UNROLL
			//#pragma HLS unroll factor=4
			//#pragma HLS PIPELINE II=10
			temp = shift_reg_v[i - 1] + x_i*b[N-i-1] - y_i*a[N-i-1];
			shift_reg_v[i] = temp;
		}

		//temp = shift_reg_v[(N-2) - 1] + x_i*b[N-(N-2)-1] - y_i*a[N-(N-2)-1];
		//shift_reg_v[N-2] = temp;
		shift_reg_v[0] = x_i*b[N-1] - y_i*a[N-1];

		AXI_VAL output;
		output.data = int96(y_i)>>25;
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






