# Contributing

NimbusPI would not exist without its contributors, and we welcome you to join us in our endeavor.  This
guide is intended for anyone who wants to contribute to the [NimbusPI](http://github.com/nimbus-pi/nimbus-pi)
project. Please read this document carefully before contributing, as it answers many of the questions that new
contributors have when first working with our projects.


## Agreement

By submitting any work to the the NimbusPI project, you agree to our [project license](LICENSE) as well as to
the following principal guidelines:

1. Any work contributed is original work or you otherwise have the right to submit the work;
1. You grant the NimbusPI project a non-exclusive, irrevocable license to use your submitted work in any way; and,
1. You are capable of granting these rights for the contribution.


## Ways to Contribute

There are many ways to contribute to NimbusPI:

* **Report a Bug** - if you find a bug, please [file a detailed issue](#bug-reports)
* **Request a Feature** - if you want to request a feature, please [file a request](#feature-requests)
* **Work on an Issue** - if you wish to contribute directly, please feel free to work on [any open issue](#working-on-issues)


### Bug Reports

Perfect code is rare, and NimbusPI is no exception.  If you find a bug, or feel something is acting
strangely, please [file an issue](https://github.com/nimbus-pi/nimbus-pi/issues/new) so that it can be
addressed.  When filing an issue, please provide the following information:

* What version of the service you were using
* What you did
* What you expected to happen
* What actually happened


### Feature Requests

We love ideas of any form.  Even if you can't add a feature on your own, we welcome all suggestions.  When making a
feature request, please [file an issue](https://github.com/nimbus-pi/nimbus-pi/issues/new) and provide the
following information:

* The feature you want to add, or problem you want to solve
* Your take on the correct approach to building the new functionality


## Working on Issues

All bugs and features are stored in our [GitHub Issues](https://github.com/nimbus-pi/nimbus-pi/issues)
section. It is here that we determine which issues will be roadmapped for various releases, and plan our
[milestones](https://github.com/nimbus-pi/nimbus-pi/milestones) accordingly.  All issues that are received
will be reviewed by the core development staff and assigned a milestone for release.

If you intend to work on a specific issue, please add a comment to the issue saying so and indicate when you think
you will complete it.  This will help us to avoid duplication of effort.  If you find that you cannot finish the work,
simply add a comment letting people know so someone else can pick it up.


### Pull Requests

All contributions to the the NimbusPI repository must go through a
[GitHub Pull Request](https://github.com/nimbus-pi/nimbus-pi/pulls).  In addition, all Pull Requests must be
directly related to an open issue.  All pull requests should follow a very specific process:

**1. Open or choose an issue to work on**

Before working, please identify or create an issue for what you are looking to contribute.  **Do note** that only
accepted issues will be merged, and if your issue is not slated for a milestone it may not be accepted.  You may
request that the issue be identified for release before you begin working.

**2. Announce that you will be working on that issue**

Let us know when you plan to start on the issue and how long you think it will take you.  This will help us be ready
to support you when it comes time to review.

**3. Fork the NimbusPI repository**

Every contributor, including core staff, is required to work within a fork of their own repository.  All branches
on the NimbusPI repository are meant for production purposes only.

**4. Add the NimbusPI upstream remote**

In order to keep your code up to date with master, you need to add the NimbusPI repostiory as your upstream:

```bash
git remote add upstream https://github.com/nimbus-pi/nimbus-pi
```

**5. Ensure that your master branch is up to date with the upstream**

```bash
git checkout master
git pull upstream master
```

**6. Create a new branch**

Create a branch on your local repository that has a descriptive name of what you are fixing, such as:

```bash
git checkout -b fix-broken-config
git push -u origin fix-broken-config
```

**7. Make your changes**

Make your changes, commit, and add tests!  All features must be tested to completion before they will be accepted.
This project makes use of JSHint, ESLint, and Mocha to provide thorough testing and code-style rules to ensure
consistency accross the project.

Please refer to our [code standards](#code-style-requirements) to save yourself time when linting!

**8. Rebase onto upstream**

Before you send a pull request, be sure to rebase onto the upstream source.  This ensures your code is running on
the latest available code.

```bash
git fetch upstream
git rebase upstream/master
```

**9. Ensure all tests pass**

After rebasing, be sure to run the test suite to make sure nothing is broken:

```bash
make test
```

It is best to ensure your coverage is of an acceptable range, as well, to ensure a positive review:

```bash
make coverage
```

This will create a report located at `htmlcov/index.html`.

**10. Squash your commits**

Commits on the production environment are used as a changelog for releases.  As such, commits must be 
[squashed](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html) to a single commit before being
accepted.

On the last step of your rebase, all commit messages must follow a specific standard to be accepted:

```
Tag: Message (fixes #issueno)
```

In this case, `Tag` is one of the following:

* `Fix` - for a bug fix
* `Update` - for any update to existing functionality
* `New` - for any new functionality
* `Docs` - for documentation updates
* `Build` - for changes to build or automation
* `Upgrade` - for dependency upgrades

Generally, you can find this tag as one of the labels on the issue you are fixing.  The `Message` should be a
one-sentence description of the change.  Finally, the issue number the Pull Request represents should be mentioned at
the end.  If the commit does not completely resolve the issue, please use `(refs #1234)` instead of `(fixes #1234)`.

Here are some good examples:

```
Build: Added new Python version to Travis-CI config (fixes #19)
Fix: Resolved bug due to extra semicolon (fixes #220)
Upgrade: Upgraded pylint package from 1.0.0 to 1.1.0 (fixes #999)
```

**11. Submit a Pull Request**

You're ready to submit your pull request!  Refer to the
[GitHub documentation](https://help.github.com/articles/creating-a-pull-request) on how best to send a pull request
from your fork.

**12. Watch for status**

All Pull Requests must pass comprehensive testing.  If the build passes or fails, it will show up on the Pull
Request.  We cannot accept any Pull Requests that fail our criteria for a build, so if that happens, please fix and
re-squash your commits, and then update the Pull Request to trigger another build.


## Code Style Requirements

All code provided to NimbusPI must follow a strict set of code standards to prevent unnecessary commit logs from
being introduced due to formatting.  NimbusPI code is based on [PEP8](https://www.python.org/dev/peps/pep-0008/),
and [pylint](https://www.pylint.org/) is used to check for compliance during testing.

Before submitting a Pull Request, `make test` must be run, provide full coverage of functionality, and successfully
pass before a request will be reviewed.


### Standards Subject to Change

With every Pull Request, the core team has the opportunity to better refine our style and acceptance guidelines.  As
such, you may be requestsed to pull an updated set of code style guidelines due to an unforseen inconsistency in
submitted code, and to resubmit your request according to the new guidelines.
