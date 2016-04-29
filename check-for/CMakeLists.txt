set(LLVM_LINK_COMPONENTS support)

add_clang_executable(check-for
  check-for.cpp
  )
target_link_libraries(check-for
  clangTooling
  clangBasic
  clangASTMatchers
  )
