# clang-format lint action

This action checks if the source code matches the `.clang-format` file.

## Inputs

### `files`

The source files to format, provided as a regex recipe.\
Default: `^.*\.(c|h|C|H|cpp|hpp|cc|hh|c++|h++|cxx|hxx)$`\
Example: `^(src)\.(h|cc)$` or `^(src|test|examples)\.(h|cc)$` for multiple.

### `clangFormatVersion`

The `clang-format` version to use. Versions 5 to 12 are available.\
Default: 9\
Example: 12

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
      uses: actions/checkout@v2

    - name: Run clang-format
      uses: PuneetMatharu/clang-format-lint-action@v0.13
      with:
        files: ^.*\.(h|c|cc|cpp)$
        clangFormatVersion: 12
        inplace: True

    - name: Commit changes
      uses: stefanzweifel/git-auto-commit-action@v4
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
      uses: actions/checkout@v2

    - name: Run clang-format
      uses: PuneetMatharu/clang-format-lint-action@v0.13
      with:
        files: ^.*\.(h|c|cc|cpp)$
        clangFormatVersion: 12
        style: chromium
```

## Run locally

Install Docker and then run:

```bash
docker build -t clang-format-lint github.com/PuneetMatharu/clang-format-lint-action
```

When the image is built, run the linting:

```bash
docker run -it --rm --workdir /src -v $(pwd):/src \
    clang-format-lint -e /clang-format/clang-format9 .
```
