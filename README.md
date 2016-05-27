## For OSX

```
brew tap homebrew/versions
brew install llvm37 --with-clang
```

Edit `~/.stack/programs/x86_64-osx/ghc-8.0.1/lib/ghc-8.0.1/settings` and point
`llc` and `opt` directly to `llvm37` versions.


