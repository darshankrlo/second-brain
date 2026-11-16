from google.genai import types
from search import search, client

def search_notes(query: str) -> str:
    """Searches the user's personal notes by the MEANING of their content.
    Describe the topic you want in plain words, like 'how Java compiles code'.
    You can also include a file name like 'lu1' to focus on one file.
    To compare documents, search once for each one.

    Args:
        query: A description of the topic to look for
    """
    print(f"[TOOL RAN] search_notes: {query}")
    hits = search(query, 4)
    return "\n\n".join(
        f"({r['source']}, chunk {r['chunk_id']}, score {score:.3f})\n{r['text']}"
        for score, r in hits
    )

SYSTEM = (
    "You are a notes assistant. For questions about the user's notes, call search_notes "
    "and answer ONLY from what it returns, naming the source files. "
    "If the results don't contain the answer, say: I couldn't find that in your notes. "
    "For greetings or small talk, answer directly without searching."
    "To compare or summarize across notes, run several searches on different topics, then combine the results. "
)

tool_map = {"search_notes": search_notes}
config = types.GenerateContentConfig(
    tools=[search_notes],
    system_instruction=SYSTEM,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

question = input("Ask your notes: ")
contents = [types.Content(role="user", parts=[types.Part(text=question)])]

for step in range(6):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=contents, config=config
    )
    calls = response.function_calls
    if not calls:
        print("\n" + response.text)
        break

    contents.append(response.candidates[0].content)
    result_parts = []
    for call in calls:
        print(f"[MODEL ASKED] {call.name}({call.args})")
        if call.name in tool_map:
            result = tool_map[call.name](**call.args)
        else:
            result = f"Error: no tool called {call.name}. Available: {list(tool_map)}"
        result_parts.append(
            types.Part.from_function_response(name=call.name, response={"result": result})
        )
    contents.append(types.Content(role="user", parts=result_parts))
