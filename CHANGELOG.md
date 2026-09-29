# CHANGELOG



## [0.1.0](https://github.com/loonghao/repo-template/compare/v0.0.1...v0.1.0) (2026-09-29)


### Features

* enhance release workflow with trusted publishing ([0a3e996](https://github.com/loonghao/repo-template/commit/0a3e9962171c610255c9492d3c3f678c7e21686c))
* make the template the new-repository baseline for the contract ([5674a28](https://github.com/loonghao/repo-template/commit/5674a28ec1a51fc209edfa85385483e0198980d4))


### Bug Fixes

* **ci:** fall back to GITHUB_TOKEN for release-please ([d1d3a7e](https://github.com/loonghao/repo-template/commit/d1d3a7e6de9658e6d518549ad08dd2df3f63129f))
* **ci:** repair the nox lint gate and the CLI return-value test ([ba0d9c5](https://github.com/loonghao/repo-template/commit/ba0d9c52651d426b6175883b9874eb81d60cc279))
* **deps:** constrain dev/docs dependencies to their supported Python range ([71941bc](https://github.com/loonghao/repo-template/commit/71941bc9b8080fedf1981c36abab5a4492aebc01))
* **deps:** constrain dev/docs dependencies to their supported Python range ([e55f149](https://github.com/loonghao/repo-template/commit/e55f1492f7cd82716b296031830496265d4b34d4))
* **deps:** express Python floors as markers so poetry 1.x can solve ([bd5cfbd](https://github.com/loonghao/repo-template/commit/bd5cfbdf59f13746af33e58f1a28d67f75994087))
* **deps:** keep python-semantic-release on 8.0.x and cap it in renovate ([#148](https://github.com/loonghao/repo-template/issues/148)) ([97c7511](https://github.com/loonghao/repo-template/commit/97c75117bec132c330dd71ca3efb5f2b63fe98f7))
* **deps:** keep requirements-dev.txt installable on Python 3.9 ([#147](https://github.com/loonghao/repo-template/issues/147)) ([64b5a8a](https://github.com/loonghao/repo-template/commit/64b5a8a2345b05279506d2bdf298cb56795fa3d7)), closes [#144](https://github.com/loonghao/repo-template/issues/144)
* **deps:** keep the 3.7/3.8 legs solvable under poetry 1.x ([0b002ee](https://github.com/loonghao/repo-template/commit/0b002eec7343fae3779ac80e265d99fef3a79f2c))
* **lint:** make the isort gate resolve and sort imports repo-wide ([8e24b41](https://github.com/loonghao/repo-template/commit/8e24b41e723586b556dcd15188ec75993cb9bb4c))
* **lint:** resolve the remaining ruff check violations ([f38554a](https://github.com/loonghao/repo-template/commit/f38554a57556bcf2deb13971ecc789058cd3eb8a))
* **test:** call main without --help so it returns instead of exiting ([78b6001](https://github.com/loonghao/repo-template/commit/78b6001520b8772b1564762e393c6ff2464663ed))


### Dependencies

* **deps-dev:** update isort requirement from &gt;=5.13.2 to &gt;=9.0.1 ([#127](https://github.com/loonghao/repo-template/issues/127)) ([d4ea2bd](https://github.com/loonghao/repo-template/commit/d4ea2bd105de2a3b0bd7e5566a344a77e25fdc29))
* **deps-dev:** update uv requirement from &gt;=0.1.0 to &gt;=0.12.19 ([c7a5d18](https://github.com/loonghao/repo-template/commit/c7a5d1875fe861b56bc22a1089230cc82dc4d0d3))

## v0.1.0 (2025-03-19)

### Chore

* chore: simplify CI configuration and update pre-commit hooks
Remove local hooks and update CI to use ubuntu-latest, simplify publish workflow

Signed-off-by: longhao &lt;hal.long@outlook.com&gt; ([`fdedeea`](https://github.com/loonghao/repo-template/commit/fdedeea511901fa95201923584cc992dc1484767))

* chore(deps): update olegtarasov/get-tag action to v2.1.4 ([`cdb25ba`](https://github.com/loonghao/repo-template/commit/cdb25ba3b59d066726112fb22108f6c4339d92cd))

* chore(deps): update codecov/codecov-action action to v5 ([`0fb7014`](https://github.com/loonghao/repo-template/commit/0fb7014784acede2630eb0bf8c7911cfc1608af5))

* chore(deps): update mariachibear/get-repo-name-action action to v1.3.0 ([`e2b9c4c`](https://github.com/loonghao/repo-template/commit/e2b9c4c43eae001fd3d33ce91f71819b5802289a))

* chore: setup continuous integration and code quality tools

Added various configuration files and workflows for continuous integration, code coverage reporting, linting, and testing. Also, updated documentation and added new scripts for release management.

Signed-off-by: longhao &lt;hal.long@outlook.com&gt; ([`ef070dc`](https://github.com/loonghao/repo-template/commit/ef070dcae6e61481df2964d4ade2ae7ab7efca6e))

### Feature

* feat: enhance release workflow with trusted publishing

Signed-off-by: longhao &lt;hal.long@outlook.com&gt; ([`0a3e996`](https://github.com/loonghao/repo-template/commit/0a3e9962171c610255c9492d3c3f678c7e21686c))

### Unknown

* Initial commit ([`8a8b15d`](https://github.com/loonghao/repo-template/commit/8a8b15d3d712a09889c9c88b1c6410e048766a82))
