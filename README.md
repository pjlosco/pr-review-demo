# PR Review Demo Project

This is a minimal demo project for the [PR Review Agent](https://github.com/pjlosco/pr-reviewer). The app is intentionally simple: a hello-world endpoint that returns two lines of text so reviewers can approve the PR quickly.

## Overview

This project demonstrates how to integrate the PR Review Agent into a GitHub repository. When you create or update a pull request, the agent will:

1. Analyze the code changes
2. (Stubbed) Fetch acceptance criteria
3. (Stubbed) Retrieve domain context
4. Generate AI-powered review comments on the PR

## Setup Instructions

### 1. Configure GitHub Secrets

Before the workflow can run, you need to add the required secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - **`OPENAI_API_KEY`**: Your OpenAI API key (required)
   - **`LANGCHAIN_API_KEY`**: Your LangSmith API key (optional, for observability)

### 2. Link PRs to Jira Tickets

To enable the agent to fetch acceptance criteria, reference Jira tickets in your PR:

- **In PR title**: `DEMO-101: Implement user authentication`
- **In PR description**: `Fixes DEMO-101` or `Related to DEMO-101`
- **As PR labels**: Add label `DEMO-101`

The agent will automatically extract ticket IDs and look them up in `stubs/jira-stubs.json`.

### 3. Test the Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/add-new-feature
   ```

2. Make some changes to the code (e.g., edit `src/auth.py`)

3. Commit and push:
   ```bash
   git add .
   git commit -m "DEMO-101: Add new authentication feature"
   git push origin feature/add-new-feature
   ```

4. Create a Pull Request on GitHub

5. The GitHub Action will automatically trigger and post review comments

## Project Structure

```
demo-product/
├── .github/
│   └── workflows/
│       └── code-review.yml    # GitHub Actions workflow
├── stubs/
│   ├── jira-stubs.json        # Jira ticket stub data
│   └── confluence-stubs.json  # Confluence page stub data
├── src/
│   ├── __init__.py
│   └── auth.py                # Sample authentication module
└── README.md
```

## Stub Data

The project includes stub data files that simulate Jira tickets and Confluence pages:

- **`stubs/jira-stubs.json`**: Contains demo tickets (DEMO-101, DEMO-102, DEMO-103)
- **`stubs/confluence-stubs.json`**: Contains demo documentation pages

You can customize these files to match your project's requirements. See the [PR Review Agent documentation](https://github.com/pjlosco/pr-reviewer/blob/main/docs/stub-data-format.md) for the format specification.

## Example PRs to Test

### Example: Hello World
- **Branch**: `feature/hello-world-demo`
- **PR Title**: `DEMO-101: Hello world demo`
- **Description**: `Updates stubs and code to a simple two-line greeting.`
- **Changes**: `src/auth.py`, `src/api.py`, `stubs/*.json`

## How It Works

1. **PR Created/Updated**: GitHub Actions workflow triggers on PR events
2. **Agent Runs**: The PR Review Agent analyzes the code changes
3. **Context Gathering**: 
   - Extracts Jira ticket IDs from PR description/title
   - Fetches acceptance criteria from stub data
   - Retrieves relevant Confluence documentation
4. **AI Review**: LLM analyzes code against acceptance criteria and domain context
5. **Comments Posted**: Review comments are posted directly on the PR

## Configuration

The workflow is configured in `.github/workflows/code-review.yml`. You can customize:

- **LLM Provider**: Change `LLM_PROVIDER` to `"anthropic"` or `"google"`
- **LLM Model**: Change `LLM_MODEL` to use different models
- **Temperature**: Adjust `LLM_TEMPERATURE` (0.0-1.0)
- **Stub Data Paths**: Modify paths if you move stub files

## Troubleshooting

### Workflow Fails with "OPENAI_API_KEY not found"
- Verify the secret is set in **Settings** → **Secrets and variables** → **Actions**
- Check the secret name matches exactly (case-sensitive)

### No Review Comments Appear
- Check the **Actions** tab for error logs
- Verify the PR URL is accessible
- Ensure workflow has `pull-requests: write` permission

### Agent Can't Find Jira/Confluence Data
- Verify stub files exist at `stubs/jira-stubs.json` and `stubs/confluence-stubs.json`
- Check that PR references ticket IDs that exist in stub data (e.g., `DEMO-101`)
- Agent will continue without Jira/Confluence context if files are missing

## Next Steps

- Customize stub data to match your project's tickets and documentation
- Add more sample code files to test different scenarios
- Experiment with different LLM models and providers
- Enable LangSmith tracing for detailed observability

## Resources

- [PR Review Agent Repository](https://github.com/pjlosco/pr-reviewer)
- [Setup Documentation](https://github.com/pjlosco/pr-reviewer/blob/main/docs/setup-demo-project.md)
- [Stub Data Format](https://github.com/pjlosco/pr-reviewer/blob/main/docs/stub-data-format.md)
- [Architecture Documentation](https://github.com/pjlosco/pr-reviewer/blob/main/docs/architecture.md)

## License

MIT License - see LICENSE file for details
