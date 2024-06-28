#include <iostream>

#include "lib.hpp"

int main() {
    const auto lib = library {};
    const auto message = "Hello from " + lib.name + "!";
    std::cout << message << '\n';
    return 0;
}
