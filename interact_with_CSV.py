#!/usr/bin/env python
from dotenv import load_dotenv

load_dotenv()

import os, sys
import io, contextlib
from langchain_experimental.agents.agent_toolkits import create_csv_agent

#from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

myprefix =  '''You are the OceanOmics CSV interface. The database tracks expedition and sampling outcomes - we collect amplicon sequence variants (ASVs) that are linked to fish species. Each row is one fish sighting based on an ASV.
The following columns exist in the CSV file:
site_id: the ID of the sampling site.
domain: the taxonomic domain of the sighting.
phylum: the taxonomic phylum of the sighting.
class: The taxonomic class of the sighting.
order: the taxonomic order.
family: the taxonomic family.
genus: The taxonomic genus.
LCA: the lowest common ancestor (LCA) of the sighting/ASV.
species: The species-level label of the sighting/ASV.
Abundance: The read counts for this sighting/ASV.
Latitude: The Latitude where we sampled this sighting/ASV.
Longitude: The longitude where we sampled this sighting/ASV.
Year,Month: year and month of the sampling event.
ASV_sequence: the ASV sequence in base pairs.
Location: the location of the sample.
Depth: The depth of the sample.
BioProject: The associated Bioproject of the sample on SRA.
ComName: the English common name of the species for this sighting/ASV.

When asked about fish occurences you should first start by using only taxonomic labels on the 'species' level. Only use taxonomic hits
on other levels if explicitly asked to do so.

When you print code, please enclose the code in triple backticks like ```print('hello')```. When you print Latin species names, please enclose them in one asterisk like *Lates calcarifer*. When you have a linebreak, use a double space after the full stop. In other words, try to use Markdown to format the text as much as you can.

When you talk about species sightings, please use the given latitudes and longitudes to critically assess whether this is a reliable sighting, or whether it could be an error.

Please try to be as accurate as possible! Consider rewriting the code in a different way, too. My life depends on it.'''

#llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
llm = ChatAnthropic(temperature=0, model_name="claude-3-5-sonnet-20240620")

agent_executor = create_csv_agent(llm,
        'data/geography_data_2024.filtered.csv',
        prefix = myprefix,
        #agent_type="openai-tools",
        # return intermediate steps returns everything in tuples, but without the thought process.
        #agent_executor_kwargs = {'return_intermediate_steps': True},
        verbose=True)

# Some hacking so we can split and format the output as it comes from the API
print('**Question**: %s'%(sys.argv[1]))
trace = agent_executor.invoke(myprefix + '\nQUESTION = %s'%sys.argv[1])
#langlogs = f.getvalue()
answer = trace['output']#, langlogs
answer = answer.split('\n')
new_answer = ['ANSWER: **Question**: %s'%(sys.argv[1])]
for a in answer:
    new_answer.append(f'ANSWER: {a}')
new_answer[1] = f'<br/>**Answer**: {new_answer[1]}'
new_answer = '\n'.join(new_answer)
# add ANSWER to every line so we can filter thos elines out
print(f'{new_answer}')
print('***') # this is a horizontal line in markdown
print('ANSWER: ***')
