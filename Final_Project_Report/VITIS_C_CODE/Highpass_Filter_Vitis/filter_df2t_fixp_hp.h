#ifndef FILTER_DF2T_FIXP_HP_H_
#define FILTER_DF2T_FIXP_HP_H_

#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include <string>
#include <iostream>
#include <stdio.h>

// Defining 32 bit axiStream
typedef ap_axis<32,1,1,1> AXI_VAL;
//Defining ap_fixed<40,8> data type for coefficients
typedef ap_fixed<40,8> coef_t;

// Defining the # of a or b coefficients
#define N 2

void filter_df2t_fixed_point_hp (
	hls::stream<AXI_VAL>& y,
	coef_t c[4],
	hls::stream<AXI_VAL>& x
	);
#endif
