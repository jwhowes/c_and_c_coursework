#pragma once
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdint.h>
#include <iostream>

__device__ __host__ void permute(uint64_t src, const int * permutation, uint64_t * dst, int permutation_len, int src_len);
__device__ void split_56(uint64_t src, uint64_t * left, uint64_t * right);
__device__ void split_64(uint64_t src, uint64_t * left, uint64_t * right);
__device__ void cycle_left(uint64_t * src, int amount, int len);

__device__ __host__ void permute(uint64_t src, const int * permutation, uint64_t * dst, int permutation_len, int src_len) {  // I'm fairly sure it works
	*dst = 0;
	for (int i = 0; i < permutation_len; i++) {
		// We set the ith bit of dst to the permutation[i]th bit of src
		*dst |= (uint64_t)(((src >> (src_len - permutation[i] - 1)) & 0x1) << (permutation_len - i - 1));
	}
}

__device__ void split_56(uint64_t src, uint64_t * left, uint64_t * right) {
	const uint64_t left_bit_mask = 0xfffffff000000000;
	const uint64_t right_bit_mask = 0xfffffff;
	*left = (src & left_bit_mask) >> 28;
	*right = src & right_bit_mask;
}

__device__ void split_64(uint64_t src, uint64_t * left, uint64_t * right) {
	const uint64_t left_bit_mask = 0xffffffff00000000;
	const uint64_t right_bit_mask = 0xffffffff;
	*left = (src & left_bit_mask) >> 32;
	*right = src & right_bit_mask;
}

__device__ void cycle_left(uint64_t * src, int amount, int len) {
	*src = (*src << amount) | (*src >> (len - amount));
}