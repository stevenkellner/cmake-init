{% if pm %}#include <catch2/catch{% if catch3 %}_test_macros{% end %}.hpp>

{% end %}#include "lib.hpp"
{% if pm %}
TEST_CASE("Name is {= name =}", "[library]") {
    const auto lib = library {};
    REQUIRE(lib.name == "{= name =}");
}{% else %}
int main() {
    const auto lib = library {};

    return lib.name == "{= name =}" ? 0 : 1;
}{% end %}
