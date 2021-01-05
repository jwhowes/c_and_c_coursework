
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <iostream>
#include <stdint.h>

#include <stdio.h>

#include "des_consts.h"
#include "bit_functions.h"

using namespace std;

__device__ void f(uint64_t right, uint64_t key, uint64_t * ret) {
	// We're just assuming all the permutations work
	permute(right, E, ret, 48);  // E goes from length 32 to length 48 (not sure if this call will work)
	*ret ^= key;
	// Apply S-boxes
	for (int i = 0; i < 6; i++) {

	}
	// Apply P permutation
	permute(*ret, P, ret, 32);
}

__device__ void des_encrypt(uint64_t block, uint64_t * keys, uint64_t * ret) {

}

__global__ void brute_force_kernel(uint64_t plaintext, uint64_t ciphertext, uint64_t * res_key, bool * done) {
	// Generate first 3 bytes of the thread's key
	uint64_t thread_key = (uint64_t)(blockIdx.x * blockDim.x + threadIdx.x) << 35;
	//const uint64_t bit_mask = 0x00FFFFF800000000;
	uint64_t keys[16];
	uint64_t PC1_permuted;
	uint64_t C;
	uint64_t D;
	uint64_t temp;
	int v;
	// First three bytes of the thread key are now fixed
	for (uint64_t i = 0; i < thread_encryptions; i++) {
		if (*done) {
			return;
		}
		// Encrypt plaintext with thread_key
		// First, obtain key schedule
		permute(thread_key, PC_1, &PC1_permuted, 56);
		split_56(PC1_permuted, &C, &D);
		for (int j = 1; j <= 16; j++) {
			if (j == 1 || j == 2 || j == 9 || j == 16) {
				v = 1;
			}else {
				v = 2;
			}
			permute((C << 32) | D, PC_2, &keys[j - 1], 48);
			cycle_left(&C, v, 28);
			cycle_left(&D, v, 28);
		}
		des_encrypt(plaintext, keys, &temp);
		if (temp == ciphertext) {
			*done = true;
			*res_key = ciphertext;
			return;
		}
		thread_key++;
	}
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