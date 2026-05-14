from dotenv import load_dotenv
from agent.orchestrator import AgentOrchestrator


load_dotenv()

def main():
    agent = AgentOrchestrator()
    user_input = input("Enter topic (or press Enter for auto generation):")

    if user_input.strip() == "":
        result = agent.run()
    else:
        result = agent.run(user_input)
        
    print("Generated Post: ", result)


if __name__ == "__main__":
    main()