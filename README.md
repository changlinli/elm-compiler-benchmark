# Benchmarking a roughly one million line Elm code base

This repository is more or less a copy of
[https://github.com/rtfeldman/elm-spa-example](https://github.com/rtfeldman/elm-spa-example),
with modifications made to allow us to make an arbitrary number of copies of
that codebase (and then merging all that code into a single `main` which gets
around Elm tree-shaking) to provide a codebase to benchmark Elm compiler
performance.

To see the README associated with the original repo, see
[./ORIGINAL_ELM_SPA_EXAMPLE_README.md](./ORIGINAL_ELM_SPA_EXAMPLE_README.md).

By default we generate 300 copies of this codebase and merge them into a single
`main`, which result in the following statistics from `tokei`.

```
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 Elm                  9901      1738804      1118404       170700       449700
===============================================================================
 Total                9901      1738804      1118404       170700       449700
===============================================================================
```

## Using this codebase

The codebase is generated by `duplicate_code.py`. If you run 
```
python duplicate_code.py
```
from within this folder, you should see a ton of files appear in `generated`.
Then you can run `$ELM_COMPILER make generated/Main.elm` and time that run
however you like to gauge performance.

## Purpose of this codebase

While developing [Zokka](https://github.com/zokka-dev/zokka-compiler), I found
it useful to have this codebase to benchmark Zokka's performance against the
vanilla Elm compiler as well as shake out any compiler bugs that might appear in
large codebases.
