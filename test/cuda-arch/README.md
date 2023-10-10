This test creates a base library requiring CUDA, then creates a downstream 
project that requires the base library, but requires a version of CUDA that uses
clang to compile source code.  This combination tests:
- The way BLT passes config flags between projects does not overwrite user-provided 
  config flags
- Users can combine user-provided flags and flags from upstream projects to configure 
  targets