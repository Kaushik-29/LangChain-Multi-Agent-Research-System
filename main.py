from src.pipelines.pipeline import run_research_pipeline

topic = input(
    "Enter Research Topic: "
)

result = run_research_pipeline(
    topic
)

print("\n")
print("=" * 80)
print("FINAL REPORT")
print("=" * 80)

print(
    result["final_report"]
)