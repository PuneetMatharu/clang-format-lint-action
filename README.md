# clang-format lint action

This action checks if the source code matches the `.clang-format` file.

## Inputs

### `files`

The source files to format, provided as a regex recipe.\
Default: `^.*\.(c|h|C|H|cpp|hpp|cc|hh|c++|h++|cxx|hxx)$`\
Example: `^(src)\.(h|cc)$` or `^(src|test|examples)\.(h|cc)$` for multiple.

### `clangFormatVersion`

What clang-format version should be used.\
Available version are\
5,6,7,8,9,10,11(11.0.0),11.0.0, 11.1.0, 12(12.0.1), 12.0.0, 12.0.1, 13(13.0.0), 13.0.0, 14(14.0.0), 14.0.0, 15(15.0.2), 15.0.2, 16(16.0.3), 16.0.0, 16.0.3, 17(17.0.4), 17.0.4, 18(18.1.8), 18.1.3, 18.1.8\
Default: 18\
Example: 15

### `style`

The style to use. Passed to the `--style` parameter of `clang-format`.\
Default: `file`\
Example: `chromium`

### `inplace`

Whether to change the files on the disk instead of writing to disk. This is the
same as `clang-format -i`.\
Default: `False`

You probably want to pair this with a GitHub action (such as [`stefanzweifel/git-auto-commit-action`](https://github.com/stefanzweifel/git-auto-commit-action)) to commit the changed files. For example:

```yml
name: Run clang-format Linter

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Run clang-format
      uses: PuneetMatharu/clang-format-lint-action@v0.17
      with:
        files: ^.*\.(h|c|cc|cpp)$
        clangFormatVersion: 18
        inplace: True

    - name: Commit changes
      uses: stefanzweifel/git-auto-commit-action@v5
      with:
        commit_user_name: clang-format-bot
        commit_message: 'Automated commit of clang-format modifications.'
```

## Example usage

```yml
name: test-clang-format

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Run clang-format
      uses: PuneetMatharu/clang-format-lint-action@v0.17
      with:
        files: ^.*\.(h|c|cc|cpp)$
        clangFormatVersion: 18
        style: chromium

    - name: Commit changes
      uses: stefanzweifel/git-auto-commit-action@v5
      with:
        commit_user_name: clang-format-bot
        commit_message: 'Automated commit of clang-format modifications.'
```

## Run locally

Install Docker and then run:

```bash
docker build -t clang-format-lint github.com/PuneetMatharu/clang-format-lint-action
```

When the image is built, run the linting:

```bash
docker run -it --rm --workdir /src -v $(pwd):/src clang-format-lint -e /clang-format/clang-format16.0.3 .
```

Actions clion format binary are from https://github.com/muttleyxd/clang-tools-static-binaries
