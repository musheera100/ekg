#ifndef FILTER_DF2T_FIXP_H_
#define FILTER_DF2T_FIXP_H_

#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <string>
#include <iostream>
#include <stdio.h>

typedef ap_axis<32,1,1,1> AXI_VAL;

#define N 7

void filter_df2t_fixp (
	hls::stream<AXI_VAL>& y,
	hls::stream<AXI_VAL>& x
	);
#endif
