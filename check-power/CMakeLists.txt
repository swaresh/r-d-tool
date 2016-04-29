set(LLVM_LINK_COMPONENTS support)

add_clang_executable(check-power
  check-power.cpp
  )
target_link_libraries(check-power
  clangTooling
  clangBasic
  clangASTMatchers
  )
