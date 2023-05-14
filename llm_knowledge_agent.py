from llm_knowledge_agent import agent, SourceNote, EvergreenNote

# TODO - add these to CLI
TEST_TEXT = """
If you’re relying on your OLTP system to provide analytics, you might be in for a surprise. While it can work initially, these systems aren’t designed to handle complex queries. Adding databases like MongoDB and CassandraDB only makes matters worse, since they’re not SQL-friendly – the language most analysts and data practitioners are used to. Over time, these systems simply can’t keep up with the demands of performing analytics.

Why does this matter? After all, data is data, right? Well, there’s a big difference between online transaction processing (OLTP) and online analytical processing (OLAP). Each has its own unique requirements in terms of software and design. That’s why solutions like Teradata and Vertica have played such a large role in many enterprises. In fact, Teradata was one of the first data warehouse systems to handle a TB of data for Walmart.

But here’s the thing: Why go through the trouble of duplicating your data and creating a separate analytics system? In this article, we’ll explore the reasons why you need to develop an analytical system if you want to answer your business questions effectively.

Access Patterns
oltp vs olap 
In order to understand the why, we first need to discuss access patterns. Access patterns refer to how data is accessed in a database system.

In OLTP systems, the access patterns are transactional, meaning that data is accessed and modified frequently in small amounts. Think about yourself as a user. You will often update your profile or create a post on your favorite social media app.

You don’t need to interact with 100,000 rows (except maybe if you need to update Twitter feeds) no you likely only need to update your information.

You’re only interacting with a small subset of the data for your single transaction. But there are likely thousands of these transactions happening at once.

Usually these are short-lived transactions that fall in the inserting, updating, or deleting of small data amounts(often referenced as CRUD).

On the other hand, in OLAP systems, the access patterns are typically analytical, meaning that data is accessed and analyzed in large amounts. OLAP systems are designed to handle complex queries that involve aggregating and summarizing large volumes of data.

These queries are usually read-only.

And instead of having thousands of users querying your database all at once you might have a dozen or so data analysts and data engineers querying the data.

Think about your baseline aggregate query where you want to find the average time your users spent watching videos on cats. That will probably hit a lot of your data storage system all at once, all to calculate how much time we spend watching cats.

Unlike OLTP, these queries don’t happen as often but they hit a large set of data.

Now that we understand the access patterns, it might be a little clearer why the systems are designed slightly differently.

Rows vs. Columns
“Not every data warehouse (OLAP) is necessarily a column store: traditional row-oriented databases and a few other architectures are also used.” – Designing Data-Intensive Applications
DDIA is right; not every data warehouse(OLAP) needs to be a column store and not every OLTP is row based. In fact, I got into an argument during an interview because I made the point that data warehouses didn’t have to be columnar.

Why then do data professionals consider column store data warehouses, true data warehouses?

Now if you haven’t heard of the term columnar database before, it’s sort of like the name suggests–the data is stored by column vs. by row.

There are several benefits that analytical queries get from having the data stored by column versus. by row. But  to understand that, it’s also helpful to apprehend how traditional row-based databases operate.

Your standard RDBMS stores data in rows, meaning all the information for said row is stored together. This makes it easy to retrieve because there is only one location that you need to pull the data from. This makes row-based databases excellent for transaction systems that often only interact with one row at a time (unless you’re running a massive delete or update).

But analytical queries generally don’t need to pull just one row, as discussed before. Instead, they might need to pull millions or billions of rows.
There is a change here, though. Instead of needing all the information on a user or transaction, many analytical queries are actually pretty straightforward (until you start building complex algorithms). But the basic BI and reporting queries answer questions like:

What was the total revenue broken down by store, product, and color?
What is the average view time on videos by category?
Which type of customer is most likely to spend more than $100?
These queries are pretty straightforward and only require a few columns. In other words, pulling all the data is unnecessary and inefficient in terms of I/O. This is not only a problem if you store the data by row, but also if you store your data by column.

Suddenly this is less of an issue.

Now, only the required columns need to be read and processed, rather than returning the entire rows. This can greatly reduce the I/O and processing requirements for large analytical queries, which are common in data warehousing.

Columnar databases also typically have advanced compression techniques specifically designed to reduce storage requirements and improve query performance. Additionally, columnar databases can leverage parallel processing and vectorization, enabling even faster query processing on modern hardware.

Now that we’ve handled the technical change, let’s talk about the logical modeling adjustment.


Data Modeling
In OLTP systems, data modeling focuses on representing the latest operational data, as well as being efficient in terms of managing the thousands of updates that could be happening every second. Thus, the data model is designed to support transactional processing and ensure data integrity.

OLTP systems typically use normalized data models, where the data is organized into highly structured tables, and the relationships between the tables are defined through primary and foreign keys. This allows for efficient data access and manipulation, which is critical for transaction processing.

In contrast, OLAP systems require a different data model type to support complex analytical queries. The data modeling in OLAP systems typically involves denormalization, which involves combining and summarizing data.

This can help simplify the analytical queries the end-user needs to write and allows for faster data retrieval. You’ll often hear terms such as star or snowflake schema be used when a bunch of data engineers and data architects are trying to design their data warehouse.
Also, you could hear reference to OBT or one-big-table, which, as the name suggests is a very wide table that has fact and dimensional data all jammed into a single table. In my experience I will often see data teams use a combination of dimensional model that eventually gets put into OBT for analysts to use.

Besides being more efficient, these models generally tend to be simpler to understand from an analyst’s perspective.

In fact, I often will see many data teams take their star or snowflake schemas and create one big table to try to reduce the number of joins required to pull data (of course, sometimes analysts don’t find this helpful).

So in theory the hardware, software and model your data could run on for transactions vs analytics might be 100% different.

And there might be a valid reason.

I could even go more in depth on other concepts such as ROLAP, MOLAP and HLAP. But for now I will stop there and hopefully its a little clearer on why.

Why Do We Replicate Data?
Can you use a replica Postgres database to run your analytics even though it’s technically an OLTP?

100%.

I have several current clients who have been running their analytics like this for a while; I even wrote about it. But eventually, your company may need to consider finding a better solution. This is generally driven by performance issues or the need to create a data layer that analysts can more easily work with.

And hopefully, you now have a better understanding of why we make the distinction between OLAP and OLTP. Many companies are trying to eliminate this difference by creating hybrid tables or making custom query languages that can query different types of data stores. But as for now, once you have a large enough data set, you’ll need to duplicate your data.

If you want to read more about data engineering and data science, then check out these articles.
"""

TEST_TEXT_2 = """
Click supports two types of parameters for scripts: options and arguments. There is generally some confusion among authors of command line scripts of when to use which, so here is a quick overview of the differences. As its name indicates, an option is optional. While arguments can be optional within reason, they are much more restricted in how optional they can be.

To help you decide between options and arguments, the recommendation is to use arguments exclusively for things like going to subcommands or input filenames / URLs, and have everything else be an option instead.
"""

TEST_TITLE = "Test Article Part 2"
TEST_TAGS = ["#test", "#nested/tag"]
TEST_DIRECTORY = "~/test"
TEST_AUTHORS = ["Sebastian Vettel"]
TEST_LINK = "https://erisianrite.com"

TEST_SOURCES = [TEST_LINK]

# agent.delete_knowledgebase()
# agent.load_knowledgebase()

enriched_text = agent.ingest_article(TEST_TEXT_2)
summary = agent.summarize_article(enriched_text)
outline = agent.generate_outline(enriched_text)
main_ideas = agent.get_main_ideas(enriched_text)

source_note = SourceNote(
    title=TEST_TITLE,
    tags=TEST_TAGS,
    text_authors=TEST_AUTHORS,
    summary=summary,
    outline=outline,
    note_directory=TEST_DIRECTORY,
    link=TEST_LINK,
)
print(source_note)

evergreen_text = agent.generate_evergreen_note_text(
    main_idea=main_ideas[0], outline=outline
)
evergreen_note = EvergreenNote(
    title=main_ideas[0],
    text=evergreen_text,
    tags=TEST_TAGS,
    note_directory=TEST_DIRECTORY,
    sources=TEST_SOURCES,
)

evergreen_note = agent.find_and_connect_related_notes(evergreen_note=evergreen_note)
evergreen_note._generate_obsidian_note()
print(evergreen_note)
