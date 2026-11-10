"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "As I was walking towards work a bird followed me from one tree to another",
            "I saw a homeless person on the street, but I was not sure if how he would use the money given to him",
            "I went to the office kitchen to get some coffee and found some candies in a basket for give away.",
            "As I was walking around the buildings, I could feel the heat of the sun directly on my skin, and wondered how field workers do everyday work",
            "I asked a finance executive to explain some calculations to me, and it seemed reasonably easy.",
            "I went out during lunch break to the lake to catch a fish, but returned empty handed.",
            "I tried to make video using AI of me trying to catch a fish and instead a dragon jumped out of the lake.",
            "The people in my neighborhood said that there was an aligator in the lake, and that they called wildlife to have someone take that aligator away",
            "On a hot day, I got in my car and was expecting the ac to cool down, but the ac did not work.",
            "I took my car to the mechanic and they gave me a discount on ac compressor replacement.",
            "I took a bingo card and found that the index number did not match the numbers before me. I asked the supervisor and she said I just got a new batcha so I had 4 numbers for index instead of three.",
            "A representative gave me a report and did not give me enough examples of what was required. I asked to give me screenshots of what was required in the report.",
            "I told my boss via text I was not feeling well and could not come to work. Then I just worked from home instead and mentioned it to him the next day.",
            "I was watching some youtube videos at home about investing, and found a lot of them but one channel had pretty good advice for every age group.",
            "I found that I could not understand a lot of text in a table. In order to understand only what I needed I printed it out and highlighted the sections I needed.",
            "I can usually get to my house using the right exit on the highway. Recently I have been getting confused by all the construction for highway widenting, so I had to use google maps.",
            "Recently I have been reviewing availabel positions sent to mail box. Sometimes I wonder how long will the job last for these technical positions that people apply to.",
            "I went to the highschool to wait for my daughter to come out of class. I found that listening to podcasts helps me in passing the time while I waited.",
            "I went to the dollar treee hoping to get some light-up sticks. When I reached at the dollar tree I found it was closed.",
            "A neightbor was selling a clothes dryer for $150. I texted him that if he would give it for $100 then I can come over and get it, he agreed.",
        ],
    },
    {
        "name": "AI group spread",
        "criterion": 2,
        # 20 clearly AI-style texts (drafted with Claude's help; see AI-use notes).
        "texts": [
            "In today's rapidly evolving digital landscape, it is essential for organizations to leverage innovative solutions that foster collaboration and drive sustainable growth.",
            'Artificial intelligence has emerged as a transformative force, offering unprecedented opportunities to enhance productivity, streamline operations, and unlock new possibilities across industries.',
            'Furthermore, it is important to note that effective communication plays a crucial role in building strong relationships and achieving long-term success in both personal and professional contexts.',
            'Climate change represents one of the most pressing challenges of our time, requiring coordinated global action, innovative technologies, and a steadfast commitment to sustainability.',
            'In conclusion, the benefits of regular exercise are multifaceted, encompassing improved physical health, enhanced mental well-being, and a greater overall quality of life.',
            'Navigating the complexities of modern education requires a holistic approach that balances academic rigor with emotional intelligence, creativity, and lifelong learning.',
            'Moreover, leveraging data-driven insights enables businesses to make informed decisions, optimize resource allocation, and maintain a competitive edge in a dynamic marketplace.',
            'Time management is a fundamental skill that empowers individuals to prioritize tasks, reduce stress, and achieve their goals with greater efficiency and confidence.',
            'The integration of renewable energy sources into the global grid presents both significant opportunities and notable challenges that stakeholders must carefully consider.',
            'Ultimately, fostering a culture of continuous improvement allows teams to adapt to change, embrace innovation, and deliver exceptional value to customers.',
            'Cybersecurity is of paramount importance in the digital age, as organizations must safeguard sensitive information against an ever-growing array of sophisticated threats.',
            'A balanced diet rich in fruits, vegetables, whole grains, and lean proteins is essential for maintaining optimal health and supporting overall well-being.',
            'Remote work has fundamentally reshaped the modern workplace, offering flexibility and autonomy while also presenting unique challenges related to collaboration and culture.',
            'By embracing diversity and inclusion, organizations can cultivate an environment where every individual feels valued, empowered, and motivated to contribute their unique perspectives.',
            'Effective leadership is characterized by clear vision, empathy, and the ability to inspire others to work collaboratively toward a shared and meaningful objective.',
            'The rise of e-commerce has revolutionized the way consumers shop, providing unparalleled convenience, a vast selection of products, and personalized experiences.',
            'In summary, mindfulness practices can significantly reduce stress, improve focus, and promote emotional resilience, making them a valuable tool for individuals from all walks of life.',
            'Sustainable urban planning plays a vital role in creating resilient, livable cities that balance economic development with environmental stewardship and social equity.',
            'It is worth noting that continuous learning and adaptability are key attributes for thriving in an increasingly interconnected and rapidly changing global economy.',
            'Overall, technology continues to reshape our world in profound ways, presenting exciting opportunities while also necessitating thoughtful consideration of ethical implications.',
        ],
    },
    {
        "name": "human group spread",
        "criterion": 2,
        # 20 clearly casual human-style texts (drafted with Claude's help).
        "texts": [
            "ok so my sister called at 6am again about the cat. he's fine. he was just under the couch the whole time lol",
            'Lost my keys twice this week. Found them in the fridge once. Not proud.',
            "Dad's truck smells like old coffee and wet dog and honestly I kind of love it.",
            'We got to the game late, parked three blocks away, and then it started pouring. Worth it though, we won by one.',
            'I burned the rice again. Smoke alarm went off, neighbor knocked, very embarrassing tuesday.',
            "My boss said 'quick question' and forty minutes later I'd agreed to run the offsite. Never again.",
            "Grandma's recipe says 'add flour until it feels right.' Feels right to who, grandma??",
            "The bus was late so I walked past the bakery and bought a croissant I didn't need. No regrets.",
            'Spent the whole sunday fixing the bike chain and it still slips on hills. Might just buy a new one.',
            "He said he'd call back in five minutes. That was last thursday.",
            'Rainy morning, stale bread, and my phone died at 4%. Great start.',
            'Honestly the movie was fine, but the guy behind us ate chips like he was being paid per crunch.',
            'I planted tomatoes in april and the squirrels have eaten every single one. Respect, I guess.',
            'Our landlord finally fixed the heater, three months and eleven emails later.',
            'Took the dog to the park and he spent twenty minutes barking at a plastic bag.',
            'My brother texted me a photo of his sandwich with no context. Ten out of ten, would receive again.',
            'Forgot my umbrella, bought another one, found the first one in my trunk. Now I own two.',
            'The elevator at work has been broken since june and somehow everyone is in a better mood.',
            'I tried yoga once. Pulled a muscle in my back lifting the mat. Done.',
            "Cousin's wedding was fun until the DJ played the same song four times.",
        ],
    },
    {
        "name": "label borderline",
        "criterion": 3,
        # 5 borderline samples. Criterion 3 = these + the 40 above, so run_eval's
        # label counts for all three scenarios together answer it.
        "texts": [
            'The meeting went well overall. We discussed the timeline, assigned the tasks, and agreed to check in again next week.',
            'I think the new policy has some benefits, but it also raises a few concerns that we should talk through before deciding.',
            'Last weekend we visited the museum, which had a good collection and a nice cafe, though it was quite crowded.',
            'Learning to cook takes practice, but with a few simple recipes and some patience anyone can get comfortable in the kitchen.',
            'The report summarizes the main findings and recommends three next steps for the team to consider in the coming quarter.',
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},                      # no text field
            {"text": "a" * 10001, "creator_id": "eval_bad_huge"},    # 10,001 chars
            {"text": "This is a normal sentence about my morning walk.", "creator_id": "eval_bad_followup"},  # must still return 200
        ],
    },

    # TODO: add what your remaining criteria need.
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
