
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <iostream>
#include <stdint.h>

#include <stdio.h>

#include "des_consts.h"
#include "bit_functions.h"

using namespace std;

__global__ void brute_force_kernel(uint64_t plaintext, uint64_t ciphertext, uint64_t * res_key, bool * done) {
	// Generate first 3 bytes of the thread's key
	uint64_t thread_id = (uint64_t)(blockIdx.x * blockDim.x + threadIdx.x);
	uint64_t thread_key = 0;
	uint64_t bit_mask = 0x7f;
	uint64_t keys[16];
	uint64_t PC1_permuted;
	uint64_t C;
	uint64_t D;
	int v;
	for (int i = 0; i < 3; i++) {
		uint64_t masked = thread_id & bit_mask;
		thread_key |= masked | (parities[masked] << 7);
		thread_key <<= 8;
		thread_id >>= 7;
	}
	thread_key <<= 32;
	// First three bytes of the thread key are now fixed
	for (uint64_t i = 0; i < thread_encryptions; i++) {
		thread_key >>= 40;
		uint64_t k = i;
		for (int j = 0; j < 5; j++) {
			uint64_t masked = k & bit_mask;
			thread_key <<= 8;
			thread_key |= masked | (parities[masked] << 7);
			k >>= 7;
		}
		// Encrypt plaintext with thread_key
		// First, obtain key schedule
		permute(thread_key, PC_1, &PC1_permuted, 64);
		split_64(PC1_permuted, &C, &D);
		for (int j = 1; j <= 16; j++) {
			if (j == 1 || j == 2 || j == 9 || j == 16) {
				v = 1;
			}else {
				v = 2;
			}
			permute((C << 32) | D, PC_2, &keys[j - 1], 64);
			cycle_left(&C, v, 32);
			cycle_left(&D, v, 32);
		}
	}
}

__device__ void des_encrypt(uint64_t block, uint64_t key, uint64_t * ret) {

}

int main() {
	uint64_t plaintext = 0x0123456789abcdef;
	uint64_t ciphertext = 0xa80f2c74f235484e;
	uint64_t plain_IP;
	permute(plaintext, IP, &plain_IP, 64);
	uint64_t cipher_FP;
	permute(ciphertext, FP, &cipher_FP, 64);
	plaintext = plain_IP;
	ciphertext = cipher_FP;
	// Instantiate CUDA variables
	uint64_t * res_key;
	bool * done;
	cudaMalloc(&res_key, sizeof(uint64_t));
	cudaMalloc(&done, sizeof(bool));
	cudaMemcpy(done, false, sizeof(bool), cudaMemcpyHostToDevice);
	brute_force_kernel <<<2048, 1024>>> (plaintext, ciphertext, res_key, done);
}