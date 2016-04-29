set(LLVM_LINK_COMPONENTS support)

add_clang_executable(check-and-or
  check-and-or.cpp
  )
target_link_libraries(check-and-or
  clangTooling
  clangBasic
  clangASTMatchers
  )
