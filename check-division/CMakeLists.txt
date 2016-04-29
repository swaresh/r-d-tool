set(LLVM_LINK_COMPONENTS support)

add_clang_executable(check-division
  check-division.cpp
  )
target_link_libraries(check-division
  clangTooling
  clangBasic
  clangASTMatchers
  )


