# npm Commands Cheatsheet

## Setup & Info

```bash
npm -v                     # npm version
node -v                        # Node version
npm init                          # interactive project setup, creates package.json
npm init -y                          # accept all defaults
npm init @scope/create-package          # scaffold from a create-* template (like create-react-app)

npm config list                # show current config
npm config get registry
npm config set registry https://registry.npmjs.org/
npm config set proxy http://proxy.example.com:8080
npm config set https-proxy http://proxy.example.com:8080
npm config delete proxy

npm doctor                # diagnose common environment issues
npm root                     # show node_modules path
npm root -g                     # global node_modules path
npm prefix                         # show npm's install prefix
```

## Installing Packages

```bash
npm install                      # install everything from package.json (uses package-lock.json if present)
npm install package                 # install + add to dependencies
npm install package@1.2.3              # specific version
npm install package@latest                # latest version regardless of current range
npm install package@next                    # next/pre-release tag

npm install --save-dev package         # add to devDependencies (-D shorthand)
npm install -D package
npm install --save-optional package       # add to optionalDependencies
npm install --global package                 # install globally (-g shorthand)
npm install -g package

npm install                     # note: --save is the default behavior since npm 5, no longer needed explicitly

npm ci                    # clean install — uses package-lock.json exactly, deletes node_modules first (CI-friendly, faster, reproducible)

npm install package --no-save        # install without modifying package.json
npm install package --legacy-peer-deps   # skip strict peer dependency resolution (npm 7+ compat escape hatch)

npm install git+https://github.com/user/repo.git       # install from a git repo
npm install ./local-package                                # install from a local path
npm install https://example.com/package.tgz                  # install from a tarball URL
```

## Uninstalling & Updating

```bash
npm uninstall package
npm uninstall -D package
npm uninstall -g package

npm update                  # update packages within the ranges specified in package.json
npm update package
npm outdated                   # show what's outdated (current, wanted, latest)

npx npm-check-updates          # check for updates BEYOND current semver ranges (separate tool, very common)
npx npm-check-updates -u          # rewrite package.json with the latest versions
npm install                          # then reinstall to apply
```

## Listing & Inspecting

```bash
npm list                    # dependency tree of the current project
npm list --depth=0             # top-level only
npm list -g --depth=0             # global packages, top-level

npm view package              # metadata about a package on the registry
npm view package versions        # all published versions
npm view package version            # latest version
npm view package dependencies

npm info package             # alias for npm view

npm audit                # security vulnerability scan
npm audit fix                # auto-fix vulnerabilities where possible
npm audit fix --force            # allow breaking changes to fix vulnerabilities
npm audit --production               # only scan production dependencies

npm fund                # show packages requesting funding
```

## package.json Scripts

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "build": "webpack --mode production",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "prebuild": "rm -rf dist",
    "postbuild": "echo Build complete"
  }
}
```

```bash
npm run start          # or just `npm start` for the special-cased scripts
npm start
npm test                  # or `npm t`
npm stop
npm restart

npm run build                # arbitrary named scripts need `run`
npm run build -- --watch         # pass extra args through to the underlying command (note the --)

npm run                     # list all available scripts

# pre/post hooks run automatically: prebuild -> build -> postbuild
```

## npx — Run Packages Without Installing Globally

```bash
npx create-react-app myapp
npx cowsay "hello"
npx package-name              # runs the package's bin, installing temporarily if not present
npx -p package-name command       # specify a different package than the command name
npx --no-install package             # fail if not already cached locally, don't fetch
```

## Workspaces (Monorepos)

```json
// root package.json
{
  "name": "my-monorepo",
  "workspaces": ["packages/*"]
}
```

```bash
npm install                          # installs all workspace packages + hoists shared deps
npm install package --workspace=packages/app-a          # install into a specific workspace
npm run build --workspace=packages/app-a                    # run a script in one workspace
npm run build --workspaces                                     # run a script in ALL workspaces
npm run build --workspaces --if-present                           # skip workspaces missing that script
```

## Publishing Packages

```bash
npm login
npm whoami

npm publish                # publish to the registry (respects "private": true in package.json to block this)
npm publish --access public       # required for scoped packages (@scope/name) on the free tier
npm publish --tag beta               # publish under a dist-tag other than "latest"
npm publish --dry-run                    # simulate without actually publishing

npm version patch          # bump patch version (1.0.0 -> 1.0.1), creates a git tag
npm version minor             # bump minor version (1.0.0 -> 1.1.0)
npm version major                # bump major version (1.0.0 -> 2.0.0)
npm version 1.2.3-beta.0            # set an exact version

npm deprecate package@"< 2.0.0" "please upgrade to v2"
npm unpublish package@1.0.0            # remove a specific version (restricted after 72 hours on npmjs.com)
```

## package.json Dependency Fields

```json
{
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "peerDependencies": {
    "react": ">=18.0.0"
  },
  "optionalDependencies": {
    "fsevents": "^2.3.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

**Version range syntax:**

| Syntax | Meaning |
|---|---|
| `1.2.3` | Exact version |
| `^1.2.3` | Compatible: `>=1.2.3 <2.0.0` (locks major) |
| `~1.2.3` | Approximately: `>=1.2.3 <1.3.0` (locks minor) |
| `>=1.2.3` | Minimum version |
| `1.2.x` | Any patch version within 1.2 |
| `*` | Any version |
| `latest` | The current `latest` dist-tag |

## Caching

```bash
npm cache verify           # verify cache integrity
npm cache clean --force       # clear npm's cache (rarely actually needed — npm self-manages this)
npm config get cache             # show cache directory location
```

## Common Gotchas

- `npm install` will update `package-lock.json` if it's out of sync with `package.json`; `npm ci` never modifies the lockfile — it fails if they're out of sync, which is exactly what you want in CI.
- Global installs (`-g`) don't affect a project's `node_modules` — CLI tools you want teammates/CI to also have should generally be devDependencies + npm scripts (or use `npx`), not global installs.
- `^` (caret) ranges can still pull in breaking changes for pre-1.0.0 packages (`^0.2.3` only allows patch updates, not minor — npm treats 0.x specially).
- `package-lock.json` should be committed to version control — it's what makes `npm ci` (and reproducible installs generally) possible.
- Peer dependency conflicts became strict in npm 7+ — `--legacy-peer-deps` is a common but blunt escape hatch; better to actually resolve the version mismatch when feasible.
- Scripts run via `npm run` execute with `node_modules/.bin` prepended to `PATH`, which is why you can call locally-installed CLI tools (like `jest`, `eslint`) directly by name inside a script without a global install.
