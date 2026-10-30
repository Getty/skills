// Original bounded integer-kernel check. No performance or model-support claim.
#include <hip/hip_runtime.h>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

static void require_hip(hipError_t status, const char* operation) {
    if (status != hipSuccess) {
        throw std::runtime_error(std::string(operation) + ": " + hipGetErrorString(status));
    }
}

__global__ void affine_kernel(const int* input, int* output, int count) {
    const int index = static_cast<int>(blockIdx.x * blockDim.x + threadIdx.x);
    if (index < count) output[index] = input[index] * 3 + 7;
}

int main(int argc, char** argv) {
    int* input_device = nullptr;
    int* output_device = nullptr;
    try {
        if (argc > 2) throw std::runtime_error("Usage: hip-smoke [visible-device-index]");
        int selected = 0;
        if (argc == 2) {
            std::size_t consumed = 0;
            selected = std::stoi(argv[1], &consumed);
            if (consumed != std::string(argv[1]).size()) throw std::runtime_error("Invalid device index");
        }
        int count = 0;
        require_hip(hipGetDeviceCount(&count), "enumerate devices");
        if (selected < 0 || selected >= count) throw std::runtime_error("No selected HIP device available");
        require_hip(hipSetDevice(selected), "select device");
        hipDeviceProp_t properties{};
        require_hip(hipGetDeviceProperties(&properties, selected), "read device properties");
        constexpr int elements = 257;  // Intentionally not a block-size multiple.
        const std::size_t bytes = elements * sizeof(int);
        std::vector<int> input(elements), output(elements, 0);
        for (int i = 0; i < elements; ++i) input[i] = (i % 101) - 50;
        require_hip(hipMalloc(reinterpret_cast<void**>(&input_device), bytes), "allocate input");
        require_hip(hipMalloc(reinterpret_cast<void**>(&output_device), bytes), "allocate output");
        require_hip(hipMemcpy(input_device, input.data(), bytes, hipMemcpyHostToDevice), "copy input");
        affine_kernel<<<(elements + 63) / 64, 64>>>(input_device, output_device, elements);
        require_hip(hipGetLastError(), "launch kernel");
        require_hip(hipDeviceSynchronize(), "complete kernel");
        require_hip(hipMemcpy(output.data(), output_device, bytes, hipMemcpyDeviceToHost), "copy result");
        for (int i = 0; i < elements; ++i) {
            if (output[i] != input[i] * 3 + 7) throw std::runtime_error("Incorrect result at element " + std::to_string(i));
        }
        require_hip(hipFree(input_device), "free input");
        input_device = nullptr;
        require_hip(hipFree(output_device), "free output");
        output_device = nullptr;
        std::cout << "PASS device=" << selected << " name=" << properties.name
                  << " elements=" << elements << " (integer kernel and copies only)\n";
        return 0;
    } catch (const std::exception& error) {
        if (input_device) (void)hipFree(input_device);
        if (output_device) (void)hipFree(output_device);
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
