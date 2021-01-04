#pragma once
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdint.h>
#include <iostream>

__device__ __host__ void permute(uint64_t src, const int * permutation, uint64_t * dst, int len);
__device__ void split_64(uint64_t src, uint64_t * left, uint64_t * right);
__device__ void cycle_left(uint64_t * src, int amount, int len);

__device__ __host__ void permute(uint64_t src, const int * permutation, uint64_t * dst, int len) {
	*dst = 0;
	for (int i = 0; i < len; i++) {
		// We set the ith bit of dst to the permutation[i]th bit of src
		*dst |= (uint64_t)(((src >> permutation[i]) & 0x1) << i);
		//*dst |= (uint64_t)((src >> (len - i) & 0x1) << permutation[i]);  // I'm fairly certain this is correct
	}
}

__device__ void split_64(uint64_t src, uint64_t * left, uint64_t * right) {
	const uint64_t left_bit_mask = 0xffffffff00000000;
	const uint64_t right_bit_mask = 0x00000000ffffffff;
	*left = (src & left_bit_mask) >> 32;
	*right = src & right_bit_mask;
}

__device__ void cycle_left(uint64_t * src, int amount, int len) {
	*src = (*src << amount) | (*src >> (len - amount));
}