# CHANGELOG

<!-- version list -->

## v0.1.0 (2025-01-20)

### Bug Fixes

- Correct branches configuration format
  ([`cd1a72c`](https://github.com/ichoosetoaccept/unifi_assist/commit/cd1a72c4eacc525fdb2f931ff5d4c410fc41ac34))

- Correct indentation in pre-commit hook update checker
  ([`18526c6`](https://github.com/ichoosetoaccept/unifi_assist/commit/18526c6a060a03b7f77b5a58b427ea98489e9afe))

- Fix invalid indentation in subprocess.run call - Move update_last_check_time call after update
  check - Improve error message for available updates

- Correct semantic-release command in workflow
  ([`cbf8656`](https://github.com/ichoosetoaccept/unifi_assist/commit/cbf86564e6c0a992939405cf0146474f9678e9f9))

The plugins should be configured in .releaserc.json, not passed as command line arguments.

- Follow semantic-release best practices
  ([`6ffe921`](https://github.com/ichoosetoaccept/unifi_assist/commit/6ffe9210548fa6f279430530eb6f83e1d95627f9))

- Add minimal package.json for semantic-release dependencies - Update workflow to follow official
  example - Keep .releaserc.json for semantic-release configuration

- Improve changelog and workflow configuration
  ([`dcc88cb`](https://github.com/ichoosetoaccept/unifi_assist/commit/dcc88cb3a8884505fb21865f499b5be704b14356))

- Remove unnecessary npm install step
  ([`97c0c27`](https://github.com/ichoosetoaccept/unifi_assist/commit/97c0c271d99ddab209280ff856d372c6d5e8e206))

We only need npx semantic-release since we're not a Node.js project

- Use exact branch name instead of regex
  ([`a1d900f`](https://github.com/ichoosetoaccept/unifi_assist/commit/a1d900f52884f6df57aad8e04036fdb83c459c7b))

- Use proper release group format for branches
  ([`a36494b`](https://github.com/ichoosetoaccept/unifi_assist/commit/a36494b1012444fbb4be7cc0c681b7a91d5d5339))

### Chores

- Allow semantic-release on test branches
  ([`a8f268e`](https://github.com/ichoosetoaccept/unifi_assist/commit/a8f268ead3b664588edda673b142c70183e9b301))

- Configure semantic release and update workflow
  ([`3fbf03f`](https://github.com/ichoosetoaccept/unifi_assist/commit/3fbf03ff60bd43c9ad50becd52ba5e1ef9bb8d98))

- Add semantic release configuration to pyproject.toml - Update GitHub Actions workflow to use
  Python semantic release - Initialize versioning and changelog management in the project

- Configure tag format to match existing tags
  ([`1a750e6`](https://github.com/ichoosetoaccept/unifi_assist/commit/1a750e6330ff7f14cc602fa5295dfb93d5de6791))

- Update dependencies and add python-semantic-release
  ([`5834c43`](https://github.com/ichoosetoaccept/unifi_assist/commit/5834c432b95c68d9338dca1e1a850a8c04a49c2c))

- Added python-semantic-release version 9.16.1 to pyproject.toml for semantic versioning. - Updated
  uv.lock with new package versions including certifi, charset-normalizer, click, and others. -
  Introduced several new packages such as dotty-dict, gitdb, gitpython, and rich to enhance project
  functionality. - Updated requests and urllib3 to their latest versions for improved security and
  performance.

### Documentation

- Fix API endpoints to match official spec
  ([`f7fe6d3`](https://github.com/ichoosetoaccept/unifi_assist/commit/f7fe6d32a177040c3d590508b5b918613f72b361))

- Update development plan with completed tasks
  ([`6ce9e7f`](https://github.com/ichoosetoaccept/unifi_assist/commit/6ce9e7f7b17a9d4dae6fbfd38d90eb5ee857e758))

- Updated PLAN.md to reflect the current status of tasks, marking completed items with checkmarks
  and ongoing tasks with construction emojis. - Enhanced documentation by detailing the
  configuration of semantic-release in .releaserc.json and the use of conventional-pre-commit for
  commit message validation. - Added sections for Git Workflow and Pre-commit Maintenance, including
  a new hook for checking pre-commit updates and configuring daily update checks. - Documented the
  release process and commit conventions in README.md for better clarity and adherence to project
  standards.

This commit improves the project's development roadmap and documentation, ensuring a clearer
  understanding of the project's setup and maintenance processes.

### Features

- Add semantic-release and pre-commit hook updates
  ([`3f39cb4`](https://github.com/ichoosetoaccept/unifi_assist/commit/3f39cb439d1cb7b9cc565a99edc944ac11c4c4b8))

- Added a new hook to for checking pre-commit hook updates, improving maintenance of the project's
  hooks. - Introduced a new
  [.releaserc.json](cci:7://file:///Users/ismar/repos/unifi_assist/.releaserc.json:0:0-0:0) file to
  configure semantic-release for automated versioning and changelog generation based on commit
  messages. - Updated to reflect the installation of semantic-release and document commit message
  guidelines, ensuring adherence to Conventional Commits. - Enhanced
  [README.md](cci:7://file:///Users/ismar/repos/unifi_assist/README.md:0:0-0:0) with detailed commit
  message guidelines to standardize contributions and improve project clarity.

This commit strengthens the project's development workflow by integrating automated release
  management and improving pre-commit hook maintenance.

- Configure semantic-release GitHub Actions workflow
  ([`91cf10c`](https://github.com/ichoosetoaccept/unifi_assist/commit/91cf10c7591e898ed8558291933fe41362eafd68))

- Added GitHub Actions workflow to run semantic-release on PR merges - Updated .releaserc.json with
  changelog and git plugins - Updated PLAN.md to reflect progress on semantic-release setup

### Refactoring

- Change changelog mode from append to update in pyproject.toml
  ([`a5b8c4a`](https://github.com/ichoosetoaccept/unifi_assist/commit/a5b8c4a78097d5af27ac1ace4ffe417b8a31cc44))

- Updated the changelog mode to ensure it replaces the existing entries instead of appending to
  them, enhancing clarity and organization of release notes.
