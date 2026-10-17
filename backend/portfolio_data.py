PORTFOLIO_CONTEXT = """
## PROFILE
Name: Balaram Naidu Chintala
Role: Associate Data Scientist at MSM Analytics (AI and data science consultancy)
Location: Hyderabad, India
Experience: 2+ years in data science and analytics. Joined MSM Analytics in
April 2024 as a Data Science Intern and became a full-time Associate Data
Scientist in October 2024.
Summary: Delivers machine learning, explainable Bayesian modelling and
Power BI analytics for insurance and risk-analytics clients. Works with Python,
scikit-learn, SQL and DAX, runs model experiments on Amazon SageMaker AI with
GitLab pipelines, and serves models through FastAPI. Also builds Generative AI
applications using LLMs, RAG and AI agent workflows. Background: Mechanical
Engineering graduate.
Contact: balaram1353naidu@gmail.com | LinkedIn: https://www.linkedin.com/in/balaram-naidu-18a116229
GitHub: https://github.com/Balaram1353

## PROFESSIONAL EXPERIENCE: OVERVIEW
MSM Analytics, Associate Data Scientist (Oct 2024 - Present); Data Science
Intern, converted to full-time (Apr 2024 - Oct 2024).
MSM Analytics is an AI and data science consultancy. Balaram contributed, as
part of the project team, to paid client engagements for Zywave, QuantivRisk
and MSIG. He contributed to these projects; he did not deliver them alone.

## CLIENT PROJECT: ZYWAVE (insurance technology) - Vehicle Insurance Premium Prediction
Problem: Premium drivers differ by state, so one nationwide model is accurate on
average but wrong in high-volume states.
- Contributed to four regression models: three state-level models plus one
  general model for the remaining US states (Python, pandas, scikit-learn).
- Cleaned client data with inconsistent formats across states; exploratory
  analysis confirmed the state-level variation that justified splitting the models.
- Ran an iterative experimentation loop: revised the modelling code, committed
  each change to GitLab and, once the GitLab pipeline passed, triggered the run
  on Amazon SageMaker AI through the AWS Console, then compared the new metrics
  with earlier runs.
- Repeated this across many code revisions until the models reached 19-30% MAPE
  (Mean Absolute Percentage Error), a metric underwriters can read as the
  average gap from the actual premium.
- Built a FastAPI service that accepts a request as JSON and returns the
  model's predicted premium, so the trained models can be used by other applications.

## CLIENT PROJECT: QUANTIVRISK (risk analytics) - Explainable Accident-Cause Model
Problem: Standard classifiers name a single accident cause, hiding that several
factors act together and giving reviewers nothing to challenge.
- Contributed to a Bayesian probabilistic model that estimates how likely each
  candidate cause (for example excessive speed) contributed to an accident,
  using only pre-accident vehicle telemetry (Python, pandas).
- Converted continuous telemetry into binary risk indicators with stated
  rule-based thresholds (for example speed >= 80 km/h), so every input to the
  model is visible and open to review.
- The output is a per-cause probability breakdown, not one verdict, so reviewers
  can interrogate and justify it.

## CLIENT PROJECT: MSIG (insurance group) - Competitive Analysis Dashboard in Power BI
Problem: Comparing a company with its competitors, cluster peers and products
meant resetting three filters by hand, so the report went unused.
- Contributed to an interactive dashboard where selecting one company
  automatically surfaces its competitors, same-cluster companies and related
  products, replacing three manual filters with a single selection.
- Designed the data model as a star schema (lookup, fact and bridge tables) and
  wrote DAX measures (CALCULATE, FILTER, SELECTEDVALUE, ALL, RANKX, SWITCH) so
  filters behave consistently across visuals.
- Added Top-N ranking by any chosen metric, year-based slicers and
  bookmark-driven buttons to add or remove comparison companies; competitor and
  cluster links are stored as explicit table rows, so they are traceable.

## PERSONAL PROJECT: SQL RAG AGENT
GitHub: https://github.com/Balaram1353/SQL-RAG-Agent
- A Retrieval-Augmented Generation (RAG) application that converts
  natural-language questions into SQL queries and retrieves answers from a
  SQLite retail transaction database using an LLM.
- Schema-aware retrieval using sentence embeddings and vector similarity search
  provides relevant database context for SQL generation.
- Uses Ollama with a locally hosted LLM for SQL generation and natural-language
  explanations of query results.
- SQL validation and read-only query execution, with safeguards against
  destructive statements, multiple SQL statements, oversized queries and
  long-running queries.
- Interactive Streamlit interface; containerized with Docker and Docker Compose.
- Automated tests cover SQL validation, query execution, agent retries and LLM
  evaluation; 19 tests pass in the local test suite.

## PERSONAL PROJECT: MINIMAL RAG SYSTEM
A learning project exploring document retrieval and large language models to
answer questions using relevant context.

## PERSONAL PROJECT: PORTFOLIO AI ASSISTANT (this chatbot)
A web chatbot with a JavaScript frontend and a FastAPI backend. It retrieves
the most relevant sections of Balaram's portfolio knowledge base and answers
visitor questions with the NVIDIA language model nvidia/nemotron-3.5-super-vl-120b-a12b.

## TECHNICAL SKILLS
- Programming and tools: Python, SQL, MySQL, SQLite, JavaScript, FastAPI,
  Streamlit, REST API integration, Docker, Docker Compose, Git, GitHub
- Machine learning and statistics: regression, Bayesian modelling, predictive
  modelling, feature engineering, scikit-learn, model evaluation (MAPE),
  exploratory data analysis
- Python libraries: pandas, NumPy, Matplotlib, Seaborn
- Cloud and MLOps practices: AWS Console, Amazon SageMaker AI, GitLab CI/CD
  pipelines, FastAPI model serving
- Business intelligence: Power BI, DAX, Power Query, star-schema data modelling,
  MS Excel, data visualisation
- Generative AI: LLMs, prompt engineering, structured outputs, tool/function
  calling, RAG with embeddings and vector search, AI agent workflows, Ollama
  (locally hosted LLMs), Claude Code for AI-assisted software development

## EDUCATION AND COURSES
- B.E. Mechanical Engineering, Vignana Bharathi Institute of Technology, Hyderabad (2023)
- Intermediate, Narayana Junior College, Hyderabad (2019)
- 10th, KVM Talent High School, Hyderabad (2017)
- Data Science course, Teachnook (Oct-Nov 2023)
- Languages: Telugu, English, Hindi

## GUIDELINES FOR THE ASSISTANT
- Answer questions about Balaram using only the retrieved context above.
- Do not invent employers, job titles, qualifications, achievements, project
  results, metrics or years of experience.
- For client work, say Balaram "contributed to" it; never claim sole ownership.
- Do not state exact salary, phone number, address or other personal details;
  say you do not have that information and point to his email or LinkedIn.
- If the context does not contain the answer, say you do not have that
  information.
- For general educational questions (for example "what is RAG?"), answer from
  general knowledge and make clear it is general information, not about Balaram.
- Be professional, helpful and concise.
"""
