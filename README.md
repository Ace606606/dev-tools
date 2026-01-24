# dev-tools
Ctrl+K Ctrl+S -> cSpell.addWordToWorkspaceSettings -> Ctrl+Alt+W


clang-tidy -p path/to/build/compile_commands/ file
run-clang-tidy -p build/ "src/my_module/.*\.cpp" -header-filter='src/my_module/.*'
-fix