#!/usr/bin/env python3

INSTRUCTIONS = """
# Task: 
You are given a Question, a model Prediction, and a list of Ground Truth answers, judge whether the model Prediction matches any answer from the list of Ground Truth answers. Follow the instructions step by step to make a judgement. 
1. If the model prediction matches any provided answers from the Ground Truth Answer list, "Accuracy" should be "True"; otherwise, "Accuracy" should be "False".
2. If the model prediction says that it couldn't answer the question or it doesn't have enough information, "Accuracy" should always be "False".
3. If the Ground Truth is "invalid question", "Accuracy" is "True" only if the model prediction is exactly "invalid question".
# Output: 
Respond with only a single JSON string with an "Accuracy" field which is "True" or "False".
"""

IN_CONTEXT_EXAMPLES = """
# Examples:
Question: how many seconds is 3 minutes 15 seconds?
Ground truth: ["195 seconds"]
Prediction: 3 minutes 15 seconds is 195 seconds.
Accuracy: True

Question: Who authored The Taming of the Shrew (published in 2002)?
Ground truth: ["William Shakespeare", "Roma Gill"]
Prediction: The author to The Taming of the Shrew is Roma Shakespeare.
Accuracy: False

Question: Who played Sheldon in Big Bang Theory?
Ground truth: ["Jim Parsons", "Iain Armitage"]
Prediction: I am sorry I don't know.
Accuracy: False
"""

FEWSHOT_COT_MOVIE = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `when was "soul" released on hulu?` (The movie "Soul" was not released on Hulu. Instead, it was released on Disney+.)
    - `what year did the simpsons stop airing?` ("The Simpsons" is an ongoing series that has been continuously airing new episodes for over three decades.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1. 
  - Question: What movies has Leonardo DiCaprio won an Oscar for?
  - References: 
    - "Leonardo DiCaprio received an Academy Award for his performance in The Revenant."
  - Thought: The references confirm DiCaprio won an Oscar for The Revenant. There’s no mention of other Oscar wins.
  - Final Answer: The Revenant.

2. 
  - Question: How many Pixar animated films were released between 2010 and 2015?
  - References:
    - "Pixar’s filmography lists 'Toy Story 3' (2010), 'Cars 2' (2011), 'Brave' (2012), 'Monsters University' (2013), and 'Inside Out' (2015)."
  - Thought: That’s 5 animated movies from 2010 to 2015. 
  - Final Answer: 5.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_SPORTS = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `what's the latest score update for OKC's game today?` (There is no game for OKC today)
    - `how many times has curry won the nba dunk contest?` (Steph Curry has never participated in the NBA dunk contest)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1. 
  - Question: Who holds the record for most points in a single NBA game?
  - References:
    - "Wilt Chamberlain scored 100 points in a single game, an NBA record."
  - Thought: That’s directly stated; no conflicting info.
  - Final Answer: Wilt Chamberlain, 100 points.

2. 
  - Question: How many World Cups has Brazil won?
  - References:
    - "Brazil has won five FIFA World Cup titles."
  - Thought: Direct info.
  - Final Answer: Five.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_FINANCE = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `what is the price of bitcoin when it launch in 2015?` (Bitcoin was launched in 2009.)
    - `which country has adopted ethereum as legal tender?` (In reality, no country has done so.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1.
  - Question: Who is the CEO of JPMorgan Chase?
  - References:
    - "Jamie Dimon has served as CEO of JPMorgan Chase since 2005."
  - Thought: Direct info again.
  - Final Answer: Jamie Dimon.

2.
  - Question: What was the total U.S. GDP in 2020, and how much did it grow in 2021?
  - References:
    - "US GDP in 2020 was $21.43 trillion."
    - "No reference to 2021 growth rate."
  - Thought: We only know 2020 GDP from references.
  - Final Answer: $21.43 trillion for 2020; growth in 2021 unknown.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MUSIC = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- If it takes too long to responsd (longer than 100000ms), you MUST respond with 'I don't know'
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `how long was phil rudd the drummer for the band van halen?` (Phil Rudd was the drummer for AC/DC, and Alex Van Halen has been the primary drummer for Van Halen.)
    - `what was the name of justin bieber's album last year?` (Justin Bieber did not release an album last year.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1.
  - Question: What songs did Whitney Houston release in the 1990s?
  - References:
    - "Whitney Houston’s 1990s albums include 'I'm Your Baby Tonight' (1990), 'The Bodyguard Soundtrack' (1992), 'Waiting to Exhale Soundtrack' (1995)."
  - Thought: Summarize key releases from references.
  - Final Answer: I’m Your Baby Tonight, The Bodyguard Soundtrack, Waiting to Exhale Soundtrack.

2.
  - Question: Who won the Grammy for Record of the Year in 2010?
  - References:
    - "The 2010 Grammy for Record of the Year went to 'Use Somebody' by Kings of Leon."
  - Thought: Direct info from references.
  - Final Answer: Kings of Leon, Use Somebody.

### Question
{query}

### References
{references}
"""

COT_PROMPT = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the question is logically/factually impossible, respond "invalid question".
- If the references do not include enough info, respond with "I don't know".
- If the references partially address the query, provide a partial answer.
- Keep chain of thought minimal under "## Thought" and final answer under "## Final Answer" in as few words as possible.

### Example:

1.
  - Question: How many continents are there on Earth?
  - References:
    - "Commonly recognized as seven continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia."
  - Thought: Straightforward from references.
  - Final Answer: Seven.

2.
  - Question: Who directed The Taming of the Shrew (2025 film)?
  - References:
    - "No mention of a 2025 film adaptation, which does not appear to exist."
  - Thought: This is a future or fictitious scenario.
  - Final Answer: invalid question.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MOVIE_KG = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `when was "soul" released on hulu?` (The movie "Soul" was not released on Hulu. Instead, it was released on Disney+.)
    - `what year did the simpsons stop airing?` ("The Simpsons" is an ongoing series that has been continuously airing new episodes for over three decades.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1. 
  - Question: What movies has Leonardo DiCaprio won an Oscar for?
  - References: 
    - "Leonardo DiCaprio received an Academy Award for his performance in The Revenant."
  - Thought: The references confirm DiCaprio won an Oscar for The Revenant. There’s no mention of other Oscar wins.
  - Final Answer: The Revenant.

2. 
  - Question: How many Pixar animated films were released between 2010 and 2015?
  - References:
    - "Pixar’s filmography lists 'Toy Story 3' (2010), 'Cars 2' (2011), 'Brave' (2012), 'Monsters University' (2013), and 'Inside Out' (2015)."
  - Thought: That’s 5 animated movies from 2010 to 2015. 
  - Final Answer: 5.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_SPORTS_KG = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `what's the latest score update for OKC's game today?` (There is no game for OKC today)
    - `how many times has curry won the nba dunk contest?` (Steph Curry has never participated in the NBA dunk contest)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1. 
  - Question: Who holds the record for most points in a single NBA game?
  - References:
    - "Wilt Chamberlain scored 100 points in a single game, an NBA record."
  - Thought: That’s directly stated; no conflicting info.
  - Final Answer: Wilt Chamberlain, 100 points.

2. 
  - Question: How many World Cups has Brazil won?
  - References:
    - "Brazil has won five FIFA World Cup titles."
  - Thought: Direct info.
  - Final Answer: Five.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_FINANCE_KG = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `what is the price of bitcoin when it launch in 2015?` (Bitcoin was launched in 2009.)
    - `which country has adopted ethereum as legal tender?` (In reality, no country has done so.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1.
  - Question: Who is the CEO of JPMorgan Chase?
  - References:
    - "Jamie Dimon has served as CEO of JPMorgan Chase since 2005."
  - Thought: Direct info again.
  - Final Answer: Jamie Dimon.

2.
  - Question: What was the total U.S. GDP in 2020, and how much did it grow in 2021?
  - References:
    - "US GDP in 2020 was $21.43 trillion."
    - "No reference to 2021 growth rate."
  - Thought: We only know 2020 GDP from references.
  - Final Answer: $21.43 trillion for 2020; growth in 2021 unknown.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MUSIC_KG = """
For the given question and the references below, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- For your final answer, please use as few words as possible. 
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- If it takes too long to responsd (longer than 100000ms), you MUST respond with 'I don't know'
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `how long was phil rudd the drummer for the band van halen?` (Phil Rudd was the drummer for AC/DC, and Alex Van Halen has been the primary drummer for Van Halen.)
    - `what was the name of justin bieber's album last year?` (Justin Bieber did not release an album last year.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1.
  - Question: What songs did Whitney Houston release in the 1990s?
  - References:
    - "Whitney Houston’s 1990s albums include 'I'm Your Baby Tonight' (1990), 'The Bodyguard Soundtrack' (1992), 'Waiting to Exhale Soundtrack' (1995)."
  - Thought: Summarize key releases from references.
  - Final Answer: I’m Your Baby Tonight, The Bodyguard Soundtrack, Waiting to Exhale Soundtrack.

2.
  - Question: Who won the Grammy for Record of the Year in 2010?
  - References:
    - "The 2010 Grammy for Record of the Year went to 'Use Somebody' by Kings of Leon."
  - Thought: Direct info from references.
  - Final Answer: Kings of Leon, Use Somebody.

### Question
{query}

### References
{references}
"""
