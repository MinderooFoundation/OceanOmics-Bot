# OceanOmics-Bot
A langchain-based wrapper for eDNA data.


Current deployment:

![deployed chatbot](https://github.com/user-attachments/assets/6548806e-b6d3-4339-89c0-f07b48af319d)


# API key

This project needs a .env file with the Anthropic API key. It looks like this:

    ANTHROPIC_API_KEY=sk-ant-blablablua

# Running this wrapper

We have this wrapper currently deployed within a Shiny app that monitors the standard output given by this script and then splits the output into different textboxes based on the script's introduced modifications of what the LLM's API returns.

We have tested this with claude-3-5-sonnet-20240620 and ChatGPT-4-turbo. 

There's a hard-coded link to a CSV with eDNA species sightings: 'data/geography_data_2024.filtered.csv', feel free to change that.

Usage:

    python interact_with_CSV.py 'Which Lutjanidae have been spotted, and are these known to occur in these areas?'

# Dependencies

Dependencies are managed via a conda environment, see langchain_env.yml.
