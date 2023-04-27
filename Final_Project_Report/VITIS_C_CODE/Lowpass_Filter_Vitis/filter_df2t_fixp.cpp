#include "filter_df2t_fixp.h"
typedef ap_fixed<32,16> data_t; //ap_fixed<32,16> data_t;
typedef ap_fixed<32,16> y_i_t; //ap_fixed<32,16> y_i_t;
typedef ap_fixed<32,16> x_i_t; //ap_fixed<32,16> x_i_t;
typedef ap_fixed<32,16> temp_t; //ap_fixed<32,16> temp_t;

using namespace std;

void filter_df2t_fixp (hls::stream<AXI_VAL>& y, coef_t c[14], hls::stream<AXI_VAL>& x) {
	#pragma HLS INTERFACE m_axi depth=14 port=c
	#pragma HLS INTERFACE axis register both port=x
	#pragma HLS INTERFACE axis register both port=y
	#pragma HLS INTERFACE ap_ctrl_none port=return

	while(1) {
		static data_t shift_reg_v[N];
		x_i_t x_i;
		y_i_t y_i;

		AXI_VAL tmp1;
		x.read(tmp1);

		//Getting current values of x, y
		x_i = x_i_t(tmp1.data);
		y_i = x_i*c[0] + shift_reg_v[N-2];

		//Multiply_Accumulate_Loop
		int i;
		for (i = N - 2; i > 0; i--) {
			#pragma HLS PIPELINE II=2
			shift_reg_v[i] = shift_reg_v[i - 1] + x_i*c[N-i-1] - y_i*c[N+N-i-1];
		}
		shift_reg_v[0] = x_i*c[N-1] - y_i*c[N+N-1];

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

