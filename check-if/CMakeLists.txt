set(LLVM_LINK_COMPONENTS support)

add_clang_executable(check-if
  check-if.cpp
  )
target_link_libraries(check-if
  clangTooling
  clangBasic
  clangASTMatchers
  )
