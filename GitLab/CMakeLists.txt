cmake_minimum_required(VERSION 3.10)
project(TestProject)


set(CMAKE_CXX_STANDARD 17)


add_library(calculator_lib
    scr/infix_calculator.cpp
    scr/postfix_calculator.cpp
    scr/linked_list.h
    scr/queue.h
    scr/stack.h
)
target_include_directories(calculator_lib PUBLIC scr)


add_executable(infix_calculator
    scr/main.cpp
    scr/infix_calculator_gui.cpp
    scr/infix_calculator_gui.h
    scr/infix_calculator.cpp
    scr/infix_calculator.h
    scr/postfix_calculator.cpp
    scr/postfix_calculator.h
    scr/linked_list.h
    scr/queue.h
    scr/stack.h
)
target_link_libraries(infix_calculator calculator_lib)


include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/release-1.11.0.zip
)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(test_calculator tests/test_calculator.cpp)
target_link_libraries(test_calculator gtest_main calculator_lib)

add_executable(test_use_case tests/test_use_case.cpp)
target_link_libraries(test_use_case gtest calculator_lib)

include(GoogleTest)
gtest_discover_tests(test_calculator)
gtest_discover_tests(test_use_case)


set(SOURCES
    scr/main.cpp
    scr/infix_calculator_gui.cpp
    scr/infix_calculator.cpp
    scr/postfix_calculator.cpp
)
add_executable(calculator ${SOURCES} ${HEADERS})


include(InstallRequiredSystemLibraries)
set(CPACK_GENERATOR "ZIP")
set(CPACK_PACKAGE_NAME "Calculator")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_CONTACT "youremail@example.com")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Calculator Application")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_SOURCE_DIR}/LICENSE")
set(CPACK_RESOURCE_FILE_README "${CMAKE_SOURCE_DIR}/README.md")

install(TARGETS calculator DESTINATION bin)
install(FILES ${HEADERS} DESTINATION include)
install(DIRECTORY docs/ DESTINATION docs)

include(CPack)

set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_SOURCE_DIR}/LICENSE")
install(DIRECTORY "${CMAKE_SOURCE_DIR}/docs" DESTINATION .)
