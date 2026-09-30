# GitHub Actions secrets required by open-pr-reviewer.
# Add these in: repository Settings -> Secrets and variables -> Actions

# 1. OPENAI_API_KEY - your OpenAI API key (required)
#    Create one at https://platform.openai.com/api-keys

# 2. GITHUB_TOKEN - usually the automatic token is enough, but if you need
#    more permissions, create a fine-grained PAT with "Pull requests: write"
#    and "Issues: write" and store it here.