#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <iostream>
#include <stdint.h>

#include <stdio.h>

#include "des_consts.h"
#include "bit_functions.h"

using namespace std;

__device__ void f(uint64_t right, uint64_t key, uint64_t * ret) {
	*ret = 0;
	const uint64_t row_mask = 0x21;
	const uint64_t col_mask = 0x1e;
	const uint64_t last_6 = 0x3f;
	uint64_t temp;
	// We're just assuming all the permutations work
	permute(right, E, &temp, 48, 32);  // E goes from length 32 to length 48 (not sure if this call will work)
	temp ^= key;
	// Apply S-boxes
	for (int i = 0; i < 8; i++) {
		int row = 0;
		int col = 0;
		// Get the last 6 bits of temp
		uint64_t row_bits = temp & row_mask;
		uint64_t col_bits = (temp & col_mask) >> 1;
		// Find row and column
		if (row_bits % 2 == 1) {
			row++;
		}
		if ((row_bits >> 5) % 2 == 1) {
			row += 2;
		}
		if (col_bits % 2 == 1) {
			col++;
		}
		col_bits >>= 1;
		if (col_bits % 2 == 1) {
			col += 2;
		}
		col_bits >>= 1;
		if (col_bits % 2 == 1) {
			col += 4;
		}
		col_bits >>= 1;
		if (col_bits % 2 == 1) {
			col += 8;
		}
		// Write the value of S box to *ret (I think maybe we have to write at the start, not at the end
		*ret |= S[i][row * 16 + col];
		*ret <<= 4;
		temp >>= 6;
	}
	*ret >>= 4;
	// Apply P permutation
	permute(*ret, P, ret, 32, 32);
}

__device__ void des_encrypt(uint64_t block, uint64_t * keys, uint64_t * ret) {
	uint64_t left;
	uint64_t right;
	uint64_t next_left;
	uint64_t f_temp;
	split_64(block, &left, &right);
	for (int i = 0; i < 16; i++) {
		next_left = right;
		f(right, keys[i], &f_temp);
		right = left ^ f_temp;
		left = next_left;
	}
	*ret = (right << 32) | left;
}

__global__ void brute_force_kernel(uint64_t plaintext, uint64_t ciphertext, uint64_t block_key, uint64_t * res_key, bool * done) {
	// Generate first 3 bytes of the thread's key
	uint64_t thread_key = block_key + ((uint64_t)(blockIdx.x * blockDim.x + threadIdx.x) << 35);
	//const uint64_t bit_mask = 0x00FFFFF800000000;
	uint64_t keys[16];
	uint64_t PC1_permuted;
	uint64_t C;
	uint64_t D;
	uint64_t temp;
	int v;
	// First three bytes of the thread key are now fixed
	if (*done) {
		return;
	}
	// Encrypt plaintext with thread_key
	// First, obtain key schedule
	permute(thread_key, PC_1, &PC1_permuted, 56, 56);
	split_56(PC1_permuted, &C, &D);
	for (int j = 1; j <= 16; j++) {
		if (j == 1 || j == 2 || j == 9 || j == 16) {
			v = 1;
		}else {
			v = 2;
		}
		permute((C << 28) | D, PC_2, &keys[j - 1], 48, 56);
		cycle_left(&C, v, 28);
		cycle_left(&D, v, 28);
	}
	des_encrypt(plaintext, keys, &temp);

	if (temp == ciphertext) {
		*done = true;
		*res_key = ciphertext;
		return;
	}
}


int main() {
	uint64_t plaintext = 0x0123456789abcdef;
	uint64_t ciphertext = 0xa80f2c74f235484e;
	uint64_t plain_IP;
	permute(plaintext, IP, &plain_IP, 64, 64);
	uint64_t cipher_FP;
	permute(ciphertext, FP, &cipher_FP, 64, 64);
	plaintext = plain_IP;
	ciphertext = cipher_FP;
	// Instantiate CUDA variables
	uint64_t * res_key;
	bool * done;
	cudaMalloc(&res_key, sizeof(uint64_t));
	cudaMalloc(&done, sizeof(bool));
	cudaMemcpy(done, false, sizeof(bool), cudaMemcpyHostToDevice);
	for (uint64_t i = 0; i < (uint64_t)1 << 46; i++) {
		brute_force_kernel <<<1, 1024>>> (plaintext, ciphertext, i << 46, res_key, done);
	}
	printf("All blocks started\n");
	cudaDeviceSynchronize();
	return 0;
}