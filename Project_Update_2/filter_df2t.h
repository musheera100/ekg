#ifndef FILTER_DF2T_H_
#define FILTER_DF2T_H_

#include <hls_stream.h>
#include <ap_axi_sdata.h>

typedef ap_axis<64,1,1,1> AXI_VAL;

#define N	7

//typedef int	coef_t;
//typedef int	data_t;

void filter_df2t (
	hls::stream<AXI_VAL>& y,
	hls::stream<AXI_VAL>& x
	);
#endif
