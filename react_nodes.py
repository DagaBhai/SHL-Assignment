import json
from base_nodes import Node
from tools import search_catalog

class ThinkNode(Node):
    def prep(self, shared):
        """
        Preparation phase: Extracts the required data from the central 'shared' dictionary.
        """
        return {"llm": shared["llm"], "messages": shared["messages"]}

    def exec(self, prep_res):
        """
        Execution phase: Performs the core action of this node.
        """
        llm = prep_res["llm"]
        messages = prep_res["messages"]
        llm_response = llm.chat_completion(messages)

        search_triggered = False
        query = None

        try:
            start = llm_response.find('{')
            if start != -1:
                json_str = llm_response[start:]
                parsed = json.loads(json_str)
                if isinstance(parsed.get("keywords"), (list, tuple)):
                    query = " ".join(str(k) for k in parsed["keywords"])
                    search_triggered = True
        except:
            pass

        if not search_triggered:
            if "keywords" in llm_response.lower():
                try:
                    import re
                    match = re.search(r'\{.*?"keywords".*?\}', llm_response, re.DOTALL)
                    if match:
                        parsed = json.loads(match.group(0))
                        query = " ".join(str(k) for k in parsed.get("keywords", []))
                        search_triggered = True
                except:
                    pass

        if search_triggered and query:
            search_results = search_catalog(query)
            
            new_messages = messages + [
                {"role": "assistant", "content": f"Catalog search for: {query}"},
                {"role": "user", "content": f"Search results: {search_results}"},
            ]
            
            final_response = llm.chat_completion(new_messages)
            return {"reply": final_response, "search_results": search_results}
        return llm_response
    
    def post(self, shared, prep_res, exec_res):
        shared["messages"].append({
            "role": "assistant",
            "content": exec_res,
            "iterations": shared["iterations"]
        })
        shared["last_reply"] = exec_res
        if shared["iterations"] >= shared["max_iterations"]:
            return "done"

        return "done"