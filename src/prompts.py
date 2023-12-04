import config


def keywords_prompt():
    return {
        "prompt": f"""\
The user will provide you with a blog post. Write down {config.keyword_count} keywords that are related to the post and also write down a small section of external links the user might \
want to look at. The links must be formatted with HTML. You will return a JSON with 2 keys: \"keywords\" and another one \"related\".
Here's one example of how you should reply:
""" + """\
[{\"keywords\": [\"keyword1\", \"keyword2\", \"keyword3\"], \"related\":  [\"<a href='https://www.abc.com/'>ABC Online Website</a>\", \"<a href='https://www.abc.com/'>ABC Online Website</a>\", \"<a href='https://www.abc.com/'>ABC Online Website</a>\", \"<a href='https://www.abc.com/'>ABC Online Website</a>\"]}}]}]
""",
        "returns_json": True,
        "mock_response": """\
      {"keywords": ["Albion", "best game", "online gaming", "sandbox game", "MMORPG", "player-driven economy", "PvP battles", "guilds", "open world", "community", "player interaction", "customization", "skills", "progression", "crafting", "gathering", "farming", "player freedom", "competitive gameplay", "player-driven economy"], "related": ["<a href=\'https://albiononline.com/\'>Albion Online Official Website</a>", "<a href=\'https://www.reddit.com/r/albiononline/\'>Albion Online Subreddit</a>", "<a href=\'https://albiononline.com/en/news\'>Albion Online News</a>", "<a href=\'https://albiononline.com/en/download\'>Albion Online Download</a>"]}\
    """,
    }


def ideas_prompt():
    return {
        "prompt": f"""\
I work for a tech blog that does articles on various subjects. Please write {config.idea_count} ideas for articles that would capture the attention of all kind of readers. The ideas should be instigating and assertive.\
Return the titles as a JSON with a key \"titles\" with an array.
""" + """\
Here's an example response: [{\"titles\": [<titles here>]}]"
""",
        "returns_json": True,
        "json_key": "titles",
        "mock_response": """\
     {"titles": [\n    "10 Essential Tips for New Albion Online Players",\n    "Mastering the PvP Combat in Albion Online: A Beginner\'s Guide",\n    "The Ultimate Resource Gathering Strategy in Albion Online",\n    "Exploring the Intriguing Lore of Albion Online: A Story Overview for New Players",\n    "Optimizing Your Builds: A Guide to Character Progression in Albion Online",\n    "Understanding the Economy of Albion Online: A Beginner\'s Guide to Trading and Crafting",\n    "Unlocking the Secrets of Albion Online\'s Open World: Tips for Exploration and Adventure",\n    "Becoming a Master Merchant: Maximizing Profits in Albion Online\'s Trading System",\n    "Albion Online\'s Guild Warfare: Formulating Strategies and Dominating the Battlefield",\n    "Advanced PvP Tactics: Outmaneuvering Opponents in Albion Online\'s GvG Battles"\n]}\
    """
    }


def hook_paragraph_prompt():
    return {
        "prompt": """\
The user will provide you with a title and sections of a blog post. Your job is to generate a small hook paragraph and kkkkkkkkkkjj questions that the user might have searched and be answered in the post.
You should write it as the user would with simple words and generic questions.
The template must be <exciting hook paragraph> <segue to questions>: <questions>"
""",
        "returns_json": False,
        "mock_response": """\
      Are you tired of the same old games and looking for something new and exciting? Look no further than Albion, the game that has been taking the gaming world by storm! If you're curious about what makes Albion so special, why it's been gaining popularity, and why now is the perfect time to dive in, then keep reading. <Why should I consider playing Albion? What sets Albion apart from other games? Why is now the best time to start playing Albion?>\
   """
    }


# def generate_titles_prompt():
#     return {
#         "prompt": f"""\
# Please provide {config.title_count} intriguing titles for posts about the user request. I'd like these titles to be engaging and reach a broad audience, but please avoid using the structure where there's a sentence followed by a colon and a sub-sentence.
# The titles should be straightforward, single sentences without breaks. Remember to be intriguing AND CONCISE, it's a simple short title.
# Your answer must be a json with a titles key.
# """,
#         "returns_json": True,
#         "json_key": "titles",
#         "mock_response": """\
#       {"titles": ["Albion Online: The Best Sandbox MMORPG", "Albion Online: The Best Sandbox MMORPG"]}\
#     """,
#     }


def generate_sections_prompt():
    return {
        "prompt": f"""\
Given the post that the user wants to write about, reply with a list of sections for each idea. Give only {config.section_count} sections for the idea.
This will help them structure their post. The sections should have intriguing titles and they should be about specific questions that the user might have on that section.
Please avoid using the structure where there's a sentence followed by a colon and a sub-sentence.
Favour how to and other tutorial type of sections. The titles should be intriguing with simple words and make it a sentence. 
Some examples include: \"How to get your first mount on Albion\" or \"The current hellgates meta and how to win all of them\" or \"Everything you need to know about Albion lore\".
""" + """\
Your answer should be a json with a sections key which is an array of strings.
Here's one example of your answer: [{\"sections\": [\"How to get your first mount on Albion\", \"The current hellgates meta and how to win all of them\", \"Everything you need to know about Albion lore\"]}]"
""",
        "returns_json": True,
        "json_key": "sections",
        "mock_response": """\
      {"sections": ["How to get your first mount on Albion", "The current hellgates meta and how to win all of them", "Everything you need to know about Albion lore"]}\
    """,
    }


def section_content_prompt():
    return {
        "prompt": """\
You are the writer of a famous and charming blog. You write about all kinds of things and you are very knowledgeable. Your end goal is to get as many views as possible.
Write down articles with information about the user initial question. Don't create sub titles and simply write 2 long paragraph about the content requested.
Remember to not give any titles or anything, just jump straight into the content. Include references to the subject in question like places, items and lore.
Assume you might be writing the middle section of an article so avoid introductory sentences or paragraphs, really go straight into what the user requested.
It should be written in a tutorial style of post so make sure to include how to do things and actionable content. You can choose to include lists IF RELEVANT. You can write in HTML and also add links to external websites
""",
        "returns_json": False,
        "mock_response": """\
      Albion Online is a sandbox MMORPG where players can do whatever they want. The game is set in a medieval fantasy world and features an open world with no loading screens or instances. Players can explore the world, fight monsters, craft items, and build their own houses. The game has a player-driven economy where players can buy and sell items with each other. Players can also form guilds and fight other guilds in PvP battles. The game is currently in alpha and is expected to be released in 2017.\
    """,
    }
