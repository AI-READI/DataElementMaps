# Best practices assessment

## 1. Project Setup

- [x] 1.1. Work from GitHub with a GitHub repository dedicated to your software in the [AI-READI organization](https://github.com/AI-READI)
- [x] 1.2. Follow GitHub best practices
- [x] 1.3. Make the GitHub repository public from day one
- [x] 1.4. Choose a license and include a LICENSE file containing standard license terms in the root of your GitHub repository
  - [x] 1.4.1. All software in the AI-READI project will be developed under the [MIT license](https://opensource.org/licenses/MIT) (unless exceptions)
- [x] 1.5. Add a README.md file in the root of your GitHub repository and include at least the following information as they become available
  - [x] 1.5.1 Brief description of the software
  - [x] 1.5.2 How to run the software (from the source code)
  - [x] 1.5.3 Inputs and outputs of the software, if applicable
  - [x] 1.5.4 Parameters, data, and data formats required to run the software, if applicable
  - [x] 1.5.5 The standards followed during development
  - [x] 1.5.6 How to report bugs/issues
  - [x] 1.5.7 Acknowledgment of NIH funding support
  - [x] 1.5.8 Other acknowledgments, if applicable
  - [x] 1.5.9 Clear attribution for authorship and software dependencies
  - [x] 1.5.10 Include [shields.io](https://shields.io) badges at the top of your README to showcase the following: license, number of contributors, number of open issues, Zenodo DOI
  - [x] 1.5.11 Include the [AI-READI logo](https://github.com/AI-READI/AI-READI-logo) at the bottom of your README

## 2. Code development

- [ ] 2.1. Follow language-specific standards and conventions when writing your code
  - [ ] 2.1.1 Python: [Python Developer's Guide](https://devguide.python.org/)
  - [ ] 2.1.2 R: [Google's R Style Guide](https://google.github.io/styleguide/Rguide.html)
  - [ ] 2.1.3 Java: [Google's Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [ ] 2.2. Use an appropriate linter for automated code quality improvements and formatting fixes
- [ ] 2.3. Give functions and variables meaningful names
- [ ] 2.4. Include comments within your code when deemed necessary for reuse.
- [ ] 2.5. If using external libraries, favor well-maintained software libraries and make sure their license is compatible with your software license
- [ ] 2.6. Record software dependencies in a requirements.txt or similar file
- [ ] 2.7. Add appropriate tests (unit, integration, and end-to-end) to all modules in your application.
- [ ]2.8. Identify and utilize tools to benchmark for accessibility such as Accessibility Insights for Web development etc.
- [ ] 2.9. Web-based software should support Modern Browsers developed with the Webkit, Blink, or Gecko rendering engines (e.g. Chrome, Safari, Firefox, MS Edge).

## 3. Pushing changes to GitHub repository

- [x] 3.1. Use two branches for your software: main and dev.
- [x] 3.2. When committing a change to the repository, make sure the change reflects a single purpose (e.g. fixing a bug or adding a new feature)
- [x] 3.3. Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/#specification)
- [x] 3.4. Make sure your git commit hooks are always run before committing to the public repository.
- [x] 3.5. When merging changes to the dev branch, create a PR from the feature or bug fix branch and invite at least one other collaborator to review the changes.

## 4. Documenting

- [x] 4.1. If more details are required to run the software from the source code in addition to what is included in the "README.md" (c.f. section 1.4.2), include them in other markdown files and refer to them in the README.
- [x] 4.2. If the software contains a user interface, maintain user documentation of the interface and identify in your README where the user documentation is located
  - [x] 4.2.1. Use the [wiki of your GitHub repository](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis) for simple software
  - [ ] 4.2.2. Build and maintain a dedicated webpage for the documentation of more complex software.
- [ ] 4.3. If your software includes an application programming interface (API), it must be documented separately as per API best practices.
- [x] 4.4. Include instructions for contributing to your software in a "CONTRIBUTING.md" file located at the root of your GitHub repository.
- [x] 4.5. Use GitHub issues to manage bugs/issues

## 5. Adding metadata

- [x] 5.1. Include metadata files:
  - [x] 5.1.1. Include a [codemeta.json](https://codemeta.github.io/) file in the root of your GitHub repository.
        Provide at least the following information: Software name (`name`), Software description/abstract (`description`), Unique identifier (`identifier`), Authors (`givenName`, `familyName`) with their Organization name (`affiliation`), Keywords (`keywords`), Programming Language (`programmingLanguage`), First and current release date (`datePublished` and `dateModified`), License used (`license`)
  - [x] 5.1.2. Include a [CITATION.cff](https://citation-file-format.github.io/) file in the root of your GitHub repository.
        Provide at least the following information: Authors (`given-names`, `family-names`) with their Organization name (`affiliation`), Software description/abstract (`abstract`), Unique identifier (`identifiers`), Keywords (`keywords`), License (`license`), Release date (`date-released`)

## 6. Version release

- [x] 6.1. Document changes between versions of your software in a "CHANGELOG.md" file located at the root of your GitHub repository
  - [x] 6.1.1. Follow the Semantic Versioning 2.0 principles outlined [here](https://semver.org) for version numbering
  - [x] 6.1.2. Follow the "[keep a changelog](https://keepachangelog.com/en/1.0.0/)" guidelines for structuring your CHANGELOG file
- [ ] 6.2. Make a GitHub release for each version of your software
  - [ ] 6.2.1. Use an automated git changelog builder based on conventional commits to document the changes for each release
- [ ] 6.3. Deposit in a language-specific repository if available:
  - [ ] 6.3.1. Python packages: [PyPI](https://pypi.org/)
  - [ ] 6.3.2. R packages: [CRAN](https://cran.r-project.org/)
  - [ ] 6.3.3. Docker-based tools: [Dockstore](https://dockstore.org/)
  - [ ] 6.3.4. JavaScript packages: [npm](https://www.npmjs.com/)
- [ ] 6.4. Deposit in a domain-specific repository if available:
  - [ ] 6.4.1. Computational neuroscience models: [ModelDB](https://senselab.med.yale.edu/ModelDB)
  - [ ] 6.4.2. R-packages aimed at the analysis of genomics data: [Bioconductor](https://www.bioconductor.org/)
- [x] 6.5. Deposit software on [Zenodo](https://zenodo.org/):
  - [x] 6.5.1. Include source code
  - [x] 6.5.2. Include executable and other files necessary to run the software if applicable
- [ ] 6.6. Share software on the [bio.tools](https://bio.tools/) registry if the software could be of interest to the larger biomedical community outside the AI-READI project

## 7. Suggested automation tools/Developer experience

- [x] 7.1. Unless you have a preferred code editor, use [VS Code](https://code.visualstudio.com/) for developing your code and include the `.vscode` directory in your GitHub repository.
- [x] 7.2. Use these VS Code extensions (or their equivalent in your preferred code editor) as applicable to your project to automatically implement some elements of the best practices:
  - [x] 7.2.1. [Better Comments](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments): Help you create more human-friendly comments and visualize them in your code.
  - [x] 7.2.2. [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint): Integrates ESLint code formatting into VS Code for Javascript projects.
  - [x] 7.2.3. [Isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort): A Visual Studio Code extension that provides import sorting for Python using isort.
  - [x] 7.2.4. [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) - Code formatter: Prettier is an opinionated code formatter. It enforces a consistent style by parsing your code and re-printing it with its own rules that take the maximum line length into account, wrapping code when necessary.
  - [x] 7.2.5. [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin): A TypeScript server plugin to make the TypeScript server know `*.vue` files.
- [ ] 7.3. Use an appropriate linter for additional code quality checks before pushing a commit (eg: [Flake](https://pypi.org/project/flake8/)/[Black](https://pypi.org/project/black/) for Python, [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)/[Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) for Javascript, etc.)
- [ ] 7.4. When adding automated testing to your application try to use the following testing frameworks if possible:
  - [ ] 7.4.1. Javascript:
    - [ ] 7.4.1.1. Unit/Integration - [Vitest](https://vitest.dev/)/[Jest](https://jestjs.io/)
    - [ ] 7.4.1.2. End-to-end - [Cypress](https://www.cypress.io/)
  - [ ] 7.4.2. Python:
    - [ ] 7.4.1.3. Unit/Integration - [pytest](https://docs.pytest.org/en/7.2.x/)
- [x] 7.5. Use [GitHub actions](https://github.com/features/actions) to automate tasks such as fixing grammatical errors, formatting code, managing GitHub issue submission, stale issues, and PRs, running unit/integration or end-to-end tests, building and releasing app/api/documentation versions on GitHub and Zenodo.
- [ ] 7.6. Use [TypeScript](https://www.typescriptlang.org/) for any web/Node.js applications instead of JavaScript where possible.
- [x] 7.7. Use [Docusaurus](https://docusaurus.io/) for developing and maintaining simple hostable development and/or user documentation
- [x] 7.8. Use [FAIRshare](https://docs.fairshareapp.io/docs/intro) to create metadata files easily, make GitHub releases, share software files on Zenodo, and register the software on bio.tools
- [ ] 7.9. Mirror repository on GitLab for backup. The AI-READI organization has GitLab sync automatically set up so no further actions are required

# Additional Information

Use this file to assess your compliance with the [best practices](https://github.com/AI-READI/software-development-best-practices) and to document any additional information that you would like to share with the AI-READI team. You may add any additional details to the checklist sections as needed.
