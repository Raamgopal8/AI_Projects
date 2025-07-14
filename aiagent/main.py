from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

# more basic operations and functions can be added...
@tool
def calculator(a:int,b:int) -> str:
    """Useful for when you need to perform a calculation."""
    print("THE Tool has been Called.")
    return f"THE SUM OF {a} AND {b} IS {a+b}."

def main():
    model = ChatOpenAI(temperature=0)

    tools = [calculator]
    agent_executor = create_react_agent(model, tools)
    
    print("WELCOME TO THE AI AGENT. Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input == "quit":
            break
        
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()
                
            