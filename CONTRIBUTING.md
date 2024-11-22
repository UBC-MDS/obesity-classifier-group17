# Contributing to the Obesity Classifier project

This outlines how to propose a change to the Obesity Classifier project.

## Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and illustrate the bug with a minimal
[reprex](https://www.tidyverse.org/help/#reprex).

## Setting Up Your Environment

Fork the repository on GitHub and then clone the fork to you local
machine. For more details on forking see the [GitHub
Documentation](https://help.github.com/en/articles/fork-a-repo).

```cmd
git clone https://github.com/UBC-MDS/obesity-classifier-group17.git
```

Make sure you have conda installed on your local machine, then execute
the following command.

```cmd
conda env create -f environment.yml
```

## Creating a Branch

Once your local environment is up-to-date, you can create a new git branch
which will contain your contribution
(always create a new branch instead of making changes to the main branch):

```cmd
git switch -c <your-branch-name>
```

## Pull request process

- We recommend that you create a Git branch for each pull request (PR).
- New code should follow the tidyverse [style guide](http://style.tidyverse.org) or PEP8 [style guide](https://www.python.org/dev/peps/pep-0008/).

## Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.

## Attribution

These contributing guidelines were adapted from:

- [dplyr contributing guidelines](https://github.com/tidyverse/dplyr/blob/master/.github/CONTRIBUTING.md)
- [altair contributing guidelines](https://github.com/vega/altair/blob/main/CONTRIBUTING.md)
