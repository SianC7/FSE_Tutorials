# Tutorial 9: Continuous Integration with GitHub Actions

In this tutorial, you will set up **Continuous Integration (CI)** for your project using **GitHub Actions**. You'll create an automated workflow that runs your test suite every time you push code, ensuring your application remains stable as you develop new features.

### Learning Objectives

- Understand what Continuous Integration (CI) is and why it's essential for software development.
- Learn how GitHub Actions automates testing and deployment workflows.
- Create a YAML configuration file to define your CI pipeline.
- Interpret test results and build status badges directly on GitHub.

---

## What is Continuous Integration (CI)?

**Continuous Integration** is a development practice where developers frequently merge their code changes into a shared repository. Each merge triggers an automated build and test process, catching bugs early and ensuring the codebase stays healthy.

Think of CI as an automated quality control system:
- **Manual Testing**: You run tests on your local machine before pushing (error-prone, easy to forget).
- **CI Testing**: Every push automatically runs all tests on a clean environment (consistent, reliable, automatic).

### Benefits of CI:
- **Catch bugs early** - Problems are detected immediately, not weeks later.
- **Faster development** - Automated testing frees you from manual checks.
- **Team confidence** - Everyone knows the main branch is stable.
- **Visibility** - Green checkmarks or red X's show build status at a glance.

---

## What is GitHub Actions?

**GitHub Actions** is a CI/CD platform built into GitHub. It allows you to automate workflows directly in your repository using YAML configuration files.

Key concepts:
- **Workflow**: An automated process defined in a `.yml` file.
- **Job**: A set of steps that run on the same virtual machine.
- **Step**: An individual task (e.g., install dependencies, run tests).
- **Runner**: A server that executes your workflow (GitHub provides free Ubuntu/Windows/macOS runners).

---

### Step 1: Check Out the tut-9 Branch

```bash
git checkout tut-9
```

---

### Step 2: Understand the Workflow Structure

Your project now has a `.github/workflows/tests.yml` file. This is where GitHub Actions looks for workflow definitions.

Let's break down what each section does:

```yaml
name: Run Tests

on:
  push:
    branches: [ main, tut-* ]
  pull_request:
    branches: [ main ]
```
- **name**: The workflow name (appears in GitHub's Actions tab).
- **on**: Triggers - when should this workflow run?
  - On pushes to `main` or any `tut-*` branch.
  - On pull requests targeting `main`.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```
- **jobs**: Defines what work to do.
- **test**: Job name (you can have multiple jobs).
- **runs-on**: Which operating system to use (ubuntu-latest is free and fast).

```yaml
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
```
- **steps**: Individual tasks within the job.
- **Checkout code**: Downloads your repository code to the runner.
- **uses**: Runs a pre-built action (checkout@v4 is maintained by GitHub).

```yaml
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
```
- **Set up Python**: Installs Python on the runner.
- **python-version**: Which Python version to use.
- **cache**: Speeds up builds by caching pip dependencies between runs.

```yaml
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
```
- **Install dependencies**: Runs shell commands.
- Upgrades pip and installs all packages from `requirements.txt`.

```yaml
    - name: Run tests with pytest
      run: |
        pytest tests/ -v --tb=short
```
- **Run tests**: Executes your test suite.
- `-v`: Verbose output (shows each test).
- `--tb=short`: Shorter traceback on failures (easier to read in CI logs).

---

### Step 3: Create the Workflow File (TODO)

**Your Task**: The workflow file is already created, but let's understand what you would do:

1. Create the directory structure: `.github/workflows/`
2. Create a file called `test.yml` inside it.
3. Copy the workflow configuration provided in the lesson or from the existing file.

**Why YAML?** It's a human-readable format perfect for configuration files. Indentation matters (like Python), and it uses key-value pairs.

---

### Step 4: Push Your Code to GitHub

```bash
git add .github/workflows/tests.yml
git commit -m "Add GitHub Actions CI workflow"
git push origin tut-9
```

---

### Step 5: Watch Your Workflow Run

1. Go to your repository on GitHub.
2. Click the **Actions** tab at the top.
3. You should see your workflow running (yellow circle = in progress, green checkmark = passed, red X = failed).
4. Click on a workflow run to see detailed logs for each step.

---

### Step 6: Verify the Workflow

Make a small change to trigger the workflow:

1. Edit a test file (e.g., add a comment in `tests/test_config.py`).
2. Commit and push:
```bash
git add tests/test_config.py
git commit -m "Trigger CI workflow"
git push origin tut-9
```
3. Go to GitHub Actions and watch the workflow run again.
4. All tests should pass (green checkmark).

---

### Step 7: Intentionally Break a Test (Learning Exercise)

Let's see what happens when tests fail:

1. Open `tests/test_transaction_class.py`.
2. Change an assertion to make it fail (e.g., change `assert True` to `assert False`).
3. Commit and push:
```bash
git add tests/test_transaction_class.py
git commit -m "Break a test intentionally"
git push origin tut-9
```
4. Go to GitHub Actions - the workflow will fail with a red X.
5. Click on the failed workflow to see which test failed and why.
6. **Important**: Revert your change and push again to fix the build:
```bash
git revert HEAD
git push origin tut-9
```

---

### Step 8: Understanding Workflow Optimization

Our workflow is optimized for free GitHub Actions usage:

- **Caching**: `cache: 'pip'` stores dependencies between runs (saves 20-30 seconds).
- **Targeted triggers**: Only runs on relevant branches (saves Actions minutes).
- **Single job**: One job is faster and uses fewer minutes than multiple jobs.
- **Ubuntu runner**: Linux runners are fastest and cheapest.

**GitHub Free Tier**: 2,000 Actions minutes/month for private repos, unlimited for public repos.

---

### Step 9: Add a Status Badge (Optional)

Show off your passing tests with a badge in your README!

1. Go to your workflow on GitHub Actions.
2. Click the "..." menu and select "Create status badge".
3. Copy the markdown code.
4. Paste it at the top of your `README.md`:

```markdown
![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/tests.yml/badge.svg)
```

Now your README will show a green "passing" badge! 🎉

---

### Step 10: Commit Everything

```bash
git add .
git commit -m "Completed Tutorial 9: GitHub Actions CI workflow"
git push origin tut-9
```

---

## Summary

- **Continuous Integration** automates testing to catch bugs early and keep your codebase stable.
- **GitHub Actions** provides free CI/CD runners that execute workflows on every push.
- **YAML workflows** define jobs, steps, and triggers in a human-readable format.
- **Workflow optimization** (caching, targeted triggers) maximizes free tier usage.
- **Status badges** provide instant visibility into your project's health.

You now have a professional CI pipeline that automatically tests your code on every push. This is the same practice used by major tech companies and open-source projects worldwide!

---

## Key Concepts Recap

### CI/CD Pipeline Flow
```
┌──────────────┐
│  git push    │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  GitHub detects push │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Spin up Ubuntu VM   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Install Python 3.11 │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Install dependencies│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Run pytest tests/   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  ✅ Pass or ❌ Fail  │
└──────────────────────┘
```

### What You Built
- Automated test execution on every push
- Multi-branch CI support (main + tutorial branches)
- Pull request validation
- Fast builds with dependency caching
- Clear test output and logs
- Professional development workflow

Congratulations! You've completed the tutorial and now have a production-ready financial application with automated testing!
