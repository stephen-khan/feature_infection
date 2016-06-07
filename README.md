#Feature Infection
> Assign new features to groups of your users while making sure that collaborators are working with the same features.

## Introduction

This project was created in response to a Khan Academy project-based interview project.  Khan Academy progressively releases new versions of code but wants to ensure that users that collaborate on the site will have the same version.

`Feature Infection` is a python library that provides the ability to apply tags across a graph of users.  The library is non-invasive, and does not require a change to existing domain models.  `Feature Infection` is designed to be used by A/B testing or Feature Choosing frameworks. 

See [this justification](./docs/subset_sum.md)

## Installation

```sh
python setup.py install
```

## Usage example

Basic usage is to create a feature, apply it to some subset of the users, then later test to see if a user has the feature.

```python
feature = feature_infection.CDC.get_infection("my-feature")
feature.limited_infection(users, len(users))
assert all(feature.is_infected(user) for user in users)
```

## Development setup

Uses pip to package dependencies.  To install run:
```sh
pip install -r requirements.txt
```

Tests are located in the `test` directory.  Run the automated tests from the project root using the command:

```sh
py.test
```
Source code standards are maintained by automated linting tools.  This project uses pylint, which is included in our pip dependencies.  (This project is also [khan-linter](https://github.com/Khan/khan-linter) clean). To run the project linter use the following command:

```sh
pylint feature_infection
```

## Release History
* 1.0.0
    * Submission for consideration for a Software Engineer position

## Meta

Distributed under the unlicense. See ``LICENSE`` for more information.

