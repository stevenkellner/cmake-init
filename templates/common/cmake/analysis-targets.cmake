set(
    ANALYSIS_PATTERNS
    source/*.c{% if cpp %}pp{% end %} source/*.h{% if cpp %}pp{% end %}
    include/*.h{% if cpp %}pp{% end %}
    test/*.c{% if cpp %}pp{% end %} test/*.h{% if cpp %}pp{% end %}{% if cpp_examples %}
    example/*.cpp example/*.hpp{% end %}{% if c_examples %}
    example/*.c example/*.h{% end %}
    CACHE STRING
    "; separated patterns relative to the project source dir to analyze"
)

set(ANALYSIS_COMMAND cppcheck CACHE STRING "Analyzer to use")

add_custom_target(
    analysis-check
    COMMAND "${CMAKE_COMMAND}"
    -D "ANALYSIS_COMMAND=${ANALYSIS_COMMAND}"
    -D "PATTERNS=${ANALYSIS_PATTERNS}"
    -P "${PROJECT_SOURCE_DIR}/cmake/analysis.cmake"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    COMMENT "Analyze the code"
    VERBATIM
)