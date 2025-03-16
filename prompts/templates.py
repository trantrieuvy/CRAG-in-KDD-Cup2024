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

COT_PROMPT = """For the given question and multiple references from web pages, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`
- If you don't know the answer, you MUST respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MOVIE_KG = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
  - `how many times has tom cruise directed a movie?` (Tom Cruise has never directed a movie.)
  - `what is the title of the movie steven spielberg released in 2025?` (Steven Spielberg has not released a movie in 2025.)
- If you don't know the answer, you MUST respond with `I don't know`
- Using the references below and prior knowledge, if there is no reference and prior knowledge, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:
1. - Question: What movies has Leonardo DiCaprio won an Oscar for?
   - Thought: Identify all movies featuring Leonardo DiCaprio, filter for Oscar wins, confirm using official records.
   - Final Answer: The Revenant.

2. - Question: How many animated movies has Pixar released?
   - Thought: Identify Pixar’s complete filmography, count animated movies, exclude non-animated works.
   - Final Answer: Total number of movies.

3. - Question: What is the runtime of "The Godfather Part II"?
   - Thought: Verify the official runtime of "The Godfather Part II" from reliable sources.
   - Final Answer: 202 minutes.

4. - Question: What was the highest-grossing movie in 2020?
   - Thought: Review global box office data for 2020, confirm the movie with the highest revenue.
   - Final Answer: Demon Slayer: Mugen Train.

### Question
{query}

### References
{references}

"""

FEWSHOT_COT_SPORTS_KG = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
  - `who scored the most goals in NBA history?` (NBA tracks points, not goals.)
  - `which team won the Super Bowl in 2024?` (Super Bowl 2024 has not yet occurred.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the references below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:
1. - Question: Who holds the record for most points scored in an NBA game?
   - Thought: Identify NBA scoring records, confirm the player and game with the highest points scored.
   - Final Answer: Wilt Chamberlain, 100 points.

2. - Question: How many World Cups has Brazil won?
   - Thought: Review FIFA World Cup records, count Brazil’s total wins, confirm using official data.
   - Final Answer: Five.

3. - Question: What team won the UEFA Champions League in 2021?
   - Thought: Identify UEFA Champions League winners for 2021, confirm using reliable sources.
   - Final Answer: Chelsea.

4. - Question: Who won the Ballon d'Or in 2019?
   - Thought: Review Ballon d'Or records for 2019, confirm the winner using reliable sources.
   - Final Answer: Lionel Messi.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_FINANCE_KG = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
  - `what was the stock price of Tesla in 1800?` (Tesla did not exist in 1800.)
  - `how much was the cryptocurrency market cap in 1900?` (Cryptocurrency did not exist in 1900.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the references below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:
1. - Question: What was the opening price of Apple stock today?
   - Thought: Review today’s stock market data, confirm Apple’s opening price.
   - Final Answer: Opening price.

2. - Question: How many companies are listed in the Dow Jones Industrial Average?
   - Thought: Identify the Dow Jones Industrial Average composition, confirm the total number of companies.
   - Final Answer: 30.

3. - Question: Who is the CEO of JPMorgan Chase?
   - Thought: Identify the current CEO of JPMorgan Chase, confirm using official company data.
   - Final Answer: Jamie Dimon.

4. - Question: What was the GDP of the United States in 2020?
   - Thought: Review U.S. GDP data for 2020, confirm the value from reliable sources.
   - Final Answer: $21.43 trillion.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MUSIC_KG = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `how long was phil rudd the drummer for the band van halen?` (Phil Rudd was the drummer for AC/DC, and Alex Van Halen has been the primary drummer for Van Halen.)
    - `what was the name of justin bieber's album last year?` (Justin Bieber did not release an album last year.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Example:
1.
    - Question: What songs did Whitney Houston release in the 1990s?
    - Thought: Identify Whitney Houston’s albums from the 1990s, list the songs from these albums, cross-check with official sources.
    - Final Answer: I'm Your Baby Tonight, The Bodyguard, Waiting to Exhale

2. 
    - Question: Who won the Grammy for Record of the Year in 2010?
    - Thought: Identify Grammy winners for Record of the Year in 2010, cross-check
    - Final Answer: Winner's name
3. 
    - Question: How many studio albums has Adele released?
    - Thought: Identify Adele’s discography, count studio albums, cross-check with official sources, exclude live and compilation albums.
    - Final Answer: Total number of studio albums.
4.
    - Question: What was the most-streamed song globally on Spotify in 2020?
    - Thought: Identify global streaming data from Spotify for 2020, confirm the song with the highest streams, verify sources.
    - Final Answer: Name of most-streamed song.


### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MOVIE = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
  - `how many times has tom cruise directed a movie?` (Tom Cruise has never directed a movie.)
  - `what is the title of the movie steven spielberg released in 2025?` (Steven Spielberg has not released a movie in 2025.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the references below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:
1. - Question: What movies has Leonardo DiCaprio won an Oscar for?
   - Thought: Identify all movies featuring Leonardo DiCaprio, filter for Oscar wins, confirm using official records.
   - Final Answer: The Revenant.

2. - Question: How many animated movies has Pixar released?
   - Thought: Identify Pixar’s complete filmography, count animated movies, exclude non-animated works.
   - Final Answer: Total number of movies.

3. - Question: What is the runtime of "The Godfather Part II"?
   - Thought: Verify the official runtime of "The Godfather Part II" from reliable sources.
   - Final Answer: 202 minutes.

4. - Question: What was the highest-grossing movie in 2020?
   - Thought: Review global box office data for 2020, confirm the movie with the highest revenue.
   - Final Answer: Demon Slayer: Mugen Train.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_SPORTS = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
  - `who scored the most goals in NBA history?` (NBA tracks points, not goals.)
  - `which team won the Super Bowl in 2024?` (Super Bowl 2024 has not yet occurred.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the references below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:

1. - Question: Who holds the record for most points scored in an NBA game?
   - Thought: Identify NBA scoring records, confirm the player and game with the highest points scored.
   - Final Answer: Wilt Chamberlain, 100 points.

2. - Question: How many World Cups has Brazil won?
   - Thought: Review FIFA World Cup records, count Brazil’s total wins, confirm using official data.
   - Final Answer: Five.

3. - Question: What team won the UEFA Champions League in 2021?
   - Thought: Identify UEFA Champions League winners for 2021, confirm using reliable sources.
   - Final Answer: Chelsea.

4. - Question: Who won the Ballon d'Or in 2019?
   - Thought: Review Ballon d'Or records for 2019, confirm the winner using reliable sources.
   - Final Answer: Lionel Messi.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_FINANCE = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note:
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
  - `what was the stock price of Tesla in 1800?` (Tesla did not exist in 1800.)
  - `how much was the cryptocurrency market cap in 1900?` (Cryptocurrency did not exist in 1900.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the references below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Examples:
1. - Question: What was the opening price of Apple stock today?
   - Thought: Review today’s stock market data, confirm Apple’s opening price.
   - Final Answer: Opening price.

2. - Question: How many companies are listed in the Dow Jones Industrial Average?
   - Thought: Identify the Dow Jones Industrial Average composition, confirm the total number of companies.
   - Final Answer: 30.

3. - Question: Who is the CEO of JPMorgan Chase?
   - Thought: Identify the current CEO of JPMorgan Chase, confirm using official company data.
   - Final Answer: Jamie Dimon.

4. - Question: What was the GDP of the United States in 2020?
   - Thought: Review U.S. GDP data for 2020, confirm the value from reliable sources.
   - Final Answer: $21.43 trillion.

### Question
{query}

### References
{references}
"""

FEWSHOT_COT_MUSIC = """For the given question and multiple references from Web Pages, think step by step, then provide the final answer.
Current date: {query_time}

Note: 
- If the query is a question, process it as instructed.
- If the query is missing or unclear, assume the user is asking a factual question.
- Avoid reinterpreting the input; proceed with answering.
- Avoid overthinking the queries and keep the answer concise.
- The user's question may contain factual errors, in which case you MUST reply `invalid question`. Here are some examples of invalid questions:
    - `how long was phil rudd the drummer for the band van halen?` (Phil Rudd was the drummer for AC/DC, and Alex Van Halen has been the primary drummer for Van Halen.)
    - `what was the name of justin bieber's album last year?` (Justin Bieber did not release an album last year.)
- If you don't know the answer, you MUST respond with `I don't know`
- If the references do not contain the necessary information to answer the question, respond with `I don't know`
- Using only the refernces below and not prior knowledge, if there is no reference, respond with `I don't know`
- Your output format needs to meet the requirements: First, start with `## Thought\n` and then output the thought process regarding the user's question. After you finish thinking, you MUST reply with the final answer on the last line, starting with `## Final Answer\n` and using as few words as possible.

### Example:
1.
    - Question: What songs did Whitney Houston release in the 1990s?
    - Thought: Identify Whitney Houston’s albums from the 1990s, list the songs from these albums, cross-check with official sources.
    - Final Answer: I'm Your Baby Tonight, The Bodyguard, Waiting to Exhale

2. 
    - Question: Who won the Grammy for Record of the Year in 2010?
    - Thought: Identify Grammy winners for Record of the Year in 2010, cross-check
    - Final Answer: Winner's name
3. 
    - Question: How many studio albums has Adele released?
    - Thought: Identify Adele’s discography, count studio albums, cross-check with official sources, exclude live and compilation albums.
    - Final Answer: Total number of studio albums.
4.
    - Question: What was the most-streamed song globally on Spotify in 2020?
    - Thought: Identify global streaming data from Spotify for 2020, confirm the song with the highest streams, verify sources.
    - Final Answer: Name of most-streamed song.

### Question
{query}

### References
{references}
"""
