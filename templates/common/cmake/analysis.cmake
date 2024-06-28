cmake_minimum_required(VERSION 3.{% if cmake_321 %}21{% else %}14{% end %})

macro(default name)
	if(NOT DEFINED "${name}")
		set("${name}" "${ARGN}")
	endif()
endmacro()

default(ANALYSIS_COMMAND cppcheck)
default(
    PATTERNS
    source/*.c{% if cpp %}pp{% end %} source/*.h{% if cpp %}pp{% end %}
    include/*.h{% if cpp %}pp{% end %}
    test/*.c{% if cpp %}pp{% end %} test/*.h{% if cpp %}pp{% end %}{% if cpp_examples %}
    example/*.cpp example/*.hpp{% end %}{% if c_examples %}
    example/*.c example/*.h{% end %}
)

file(GLOB_RECURSE files ${PATTERNS})

foreach(file IN LISTS files)
    execute_process(
        COMMAND "${ANALYSIS_COMMAND}" --cppcheck-build-dir=build "${file}"
        WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    )
endforeach()