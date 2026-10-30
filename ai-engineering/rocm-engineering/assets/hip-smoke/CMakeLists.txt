cmake_minimum_required(VERSION 3.24)
project(rocm_smoke LANGUAGES CXX HIP)

add_executable(hip-smoke hip-smoke.hip)
set_target_properties(hip-smoke PROPERTIES HIP_STANDARD 17 HIP_STANDARD_REQUIRED YES)
enable_testing()
add_test(NAME hip-smoke-correctness COMMAND hip-smoke)
