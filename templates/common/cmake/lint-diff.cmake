cmake_minimum_required(VERSION 3.{% if cmake_321 %}21{% else %}14{% end %})

macro(default name)
	if(NOT DEFINED "${name}")
		set("${name}" "${ARGN}")
	endif()
endmacro()

default(PYTHON_EXECUTABLE python)
default(
    PATTERNS
    source/*.c{% if cpp %}pp{% end %} source/*.h{% if cpp %}pp{% end %}
    include/*.h{% if cpp %}pp{% end %}
    test/*.c{% if cpp %}pp{% end %} test/*.h{% if cpp %}pp{% end %}{% if cpp_examples %}
    example/*.cpp example/*.hpp{% end %}{% if c_examples %}
    example/*.c example/*.h{% end %}
)

file(GLOB_RECURSE files ${PATTERNS})

set(FORMAT_VALID 0)

foreach(file IN LISTS files)
    execute_process(
        COMMAND "${PYTHON_EXECUTABLE}" ./scripts/run-clang-format.py --color always "${file}"
        WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
        RESULT_VARIABLE result
        OUTPUT_VARIABLE output
    )

    if(NOT result EQUAL "0")
        set(FORMAT_VALID 1)
        message("\nThe file ${file} needs to be fixed:")
        message(${output})
    endif()
endforeach()

if(FORMAT_VALID EQUAL 0)
    message("\nAll files are correctly formatted.")
else()
    message("\nSome files need to be fixed. Run the following CMAKE target to fix them: format-fix")
endif()