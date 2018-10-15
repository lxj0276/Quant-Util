## What *should* be checked in

* Shared code
* For each of you:
  * Project specific code
  * iPython notebooks


## What *should NOT* be checked in

* Data
  * Even a small text file containing a list of stocks
  * Data should be put onto the server and referred from the experiments by relative paths (probably via a symlink)


# Directory structure

* **quantlab** - The main directory for source code. Sub-directories are allowed.

* **tests** - The main directory for tests.
  * (For Mac and Linux) Contains a symlink to quantlab so that all tests can directly do `import quantlab`.

* **projects** - The main directory for all the projects. Each project should be in a sub-directory.
