# llm-knowledge-agent

An agent to research a given topic by doing analytical and syntopic reading, summarizing and extracting main points, connecting them together, 
and forming new knowledge outputs such as zettels or evergreen notes.

## Installation
Clone this repo and use `poetry install`.

## Use

### Before first use
1. Copy the `example.env` file to `.env` and fill out your keys.
2. Run `load_knowledgebase` command to create and store your evergreen note embeddings.

### Creating a note
1. Create a textfile [in this format](#article-file-format) for your article.
2. Run `make_article --f FILE_LOCATION` and your source and evergreen notes will be added to the directories you specified in `.env`

## Warnings
- This is mostly a prototype to learn about building LLMs. With paid API access, this could get very costly very quickly and has not yet been optimized for cost-effectiveness.
- The current version is built for Obsidian-based knowledgebases, but there is an open issue for supporting additional tools for thought.
- This is also built around my own source and evergreen note templates. Feel free to rework the templates in `llm_knowledge_agent/obsidian_templates.py` to fit your templates. In the future this will be easier to configure.

## Article file format
TITLE  
AUTHORS (separated by commas)  
TAGS (#format separated by commas)  
URL  
TEXT  
