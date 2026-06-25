from json import tool

from backend.tools.registry import TOOLS


class Executor:

    def execute(self, plan: list, state: dict):

        results = []

        for step in plan:

            tool = TOOLS.get(step)

            if not tool:
                continue

            if step == "summarize":
                if state.get("summary"):
                    print("Skipping duplicate summarize")
                    continue

            print(f"Executing: {step}")

            #pass state to every tool
            state = tool(state)
            if plan == ["conversation"]:
                return tool(state), [{"step": "conversation", "state": state}]

            results.append({
                "step": step,
                "state": state
            })

        return state, results
    
