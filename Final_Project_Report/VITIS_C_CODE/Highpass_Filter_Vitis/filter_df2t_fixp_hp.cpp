#include "filter_df2t_fixp_hp.h"
typedef ap_fixed<32,16> data_t;
typedef ap_fixed<32,16> y_i_t;
typedef ap_fixed<32,16> x_i_t;
typedef ap_fixed<32,16> temp_t;

using namespace std;

void filter_df2t_fixed_point_hp (hls::stream<AXI_VAL>& y, coef_t c[4], hls::stream<AXI_VAL>& x) {
	#pragma HLS INTERFACE m_axi depth=4 port=c
	#pragma HLS INTERFACE axis register both port=x
	#pragma HLS INTERFACE axis register both port=y
	#pragma HLS INTERFACE ap_ctrl_none port=return

	while(1) {
		#pragma HLS PIPELINE II=3

		static x_i_t x_i;
		static y_i_t y_i;

		AXI_VAL tmp1;
		x.read(tmp1);

		y_i = x_i_t(tmp1.data)*c[0] + x_i*c[1] - y_i*c[3];
		x_i = x_i_t(tmp1.data);

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

