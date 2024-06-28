#include <string>

#include "{= name =}/{= name =}.hpp"
{% if pm %}
#include <catch2/catch{% if catch3 %}_test_macros{% end %}.hpp>

TEST_CASE("Name is {= name =}", "[library]") {
    const auto exported = exported_class {};
    REQUIRE(std::string("{= name =}") == exported.name());
}{% else %}
int main() {
    const auto exported = exported_class {};

    return std::string("{= name =}") == exported.name() ? 0 : 1;
}{% end %}
