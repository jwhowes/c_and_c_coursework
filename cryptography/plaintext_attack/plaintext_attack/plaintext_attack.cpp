#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <array>
#include <iostream>
#include <chrono>
#include <cstdio>
#include <wchar.h>
#include <process.h>
#include <Windows.h>
#include <thread>
#include <vector>

using namespace std;

const int num_words = 13495;

string words[num_words];

int pairs[num_words * num_words][2];

bool passed[num_words * num_words];

const string path = "C:/Users/taydo/OneDrive/Documents/computer_science/year3/C_and_C/coursework/cryptography/";
const char * exec_name = "C:/Users/taydo/OneDrive/Documents/computer_science/year3/C_and_C/coursework/cryptography/encrypt.exe";

void check_encrypt(char * plain, int index) {
	string enc = "";
	FILE* pipe = _popen((path + "encrypt.exe " + plain).c_str(), "r");
	char buffer[17];
	if (pipe) {
		fgets(buffer, sizeof buffer, pipe) != NULL;
		enc += buffer;
	}
	// If plain encrypted = the first 8 bytes of the ciphertext then bool[i] = true
		// where i is the position of pair in pairs
	// if enc == "903408ec4d951acf", write index to file (we can recover the full plaintexts later)
	passed[index] = enc == "903408ec4d951acf";
}

bool eq(char * str1, char * str2) {
	for (int i = 0; i < 16; i++) {
		if (str1[i] != str2[i]) {
			return false;
		}
	}
	return true;
}

int main(){
	vector<thread> threads;
	auto start = chrono::high_resolution_clock::now();
	ifstream ifile;
	ifile.open(path + "words.txt");
	if (ifile.is_open()) {
		for(int i = 0; i < num_words; i++){
			ifile >> words[i];
		}
	}
	int pos = 0;
	for (int i = 0; i < num_words; i++) {
		for (int j = 0; j < num_words; j++) {
			pairs[pos][0] = i;
			pairs[pos][1] = j;
			pos++;
		}
	}
	// Map check_encrypt over pairs
	char plain[17];
	for (int i = 0; i < num_words * num_words; i++) {
		string full = words[pairs[i][0]] + "." + words[pairs[i][1]];
		string temp = full.substr(0, 8);
		stringstream plain_hex;
		for (string::size_type j = 0; j < temp.length(); j++) {
			plain_hex << hex << (int)temp[j];
		}
		for (int j = 0; j < 16; j++) {
			plain[j] = plain_hex.str()[j];
		}
		plain[16] = 0;
		threads.emplace_back(thread(check_encrypt, plain, i));
	}
	cout << "all threads started!" << endl;
	for (auto & th : threads) {
		th.join();
	}
	// Write pairs that pass to output file
	for (int i = 0; i < num_words * num_words; i++) {
		if (passed[i]) {
			// write words[pairs[i][0]] + "." + words[pairs[i][1]] to output file
		}
	}
	cout << "Time taken (ms): " << chrono::duration_cast<chrono::microseconds>(chrono::high_resolution_clock::now() - start).count() << endl;
	// Current best for 10 words is 10500192 ms
	return 0;
}