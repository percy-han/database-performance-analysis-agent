from strands import Agent
from strands_tools import shell, current_time, file_read, image_reader
from strands.models import BedrockModel
from botocore.config import Config as BotocoreConfig
from plot_diagram_tool import plot_diagram_tool
from snapshot_queries_tool import snapshot_queries_tool
from database_schema_tool import database_schema_tool
from strands.agent.conversation_manager import SummarizingConversationManager


SYSTEM_PROMPT = '''
You are a MySQL database performance analyst diagnosing CPU usage spikes.

## Diagnostic Process

1. **Analyze Diagrams**: Use plot_diagram_tool to examine CPU, deleted/inserted/updated/read rows patterns.

2. **Pattern Correlation**: Evaluate similarity using:
   - Timing alignment (±5% window)
   - Shape similarity
   - Magnitude correlation
   If ALL 3 criteria met with 80%+ score, proceed. Otherwise STOP.

3. **Slow Query Investigation** (only if correlation ≥80%):
   - READ only → use snapshot_queries_tool
   - Any WRITE operations → check PixPin_2025-05-27_21-24-57.png

4. **Root Cause**: Identify query with highest (execution_time × frequency). Use database_schema_tool for analysis.

Be concise, quantify observations, provide numerical evidence.
'''
# Create the summarizing conversation manager with default settings
conversation_manager = SummarizingConversationManager(
    summary_ratio=0.3,  # Summarize 30% of messages when context reduction is needed
    preserve_recent_messages=5,  # Always keep 5 most recent messages (减少以节省token)
)


# Create a boto client config with custom settings
boto_config = BotocoreConfig(
    retries={"max_attempts": 10, "mode": "standard"},
    connect_timeout=5,
    read_timeout=600
)

# Create a configured Bedrock model
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name="us-east-1",  # Specify a different region than the default
    temperature=0.1,
    top_p=0.1,
    boto_client_config=boto_config,
    max_tokens=4096  # 限制每次输出的最大token数
)

agent = Agent(
    tools=[shell, current_time, file_read, image_reader, plot_diagram_tool, snapshot_queries_tool, database_schema_tool],
    conversation_manager=conversation_manager,  # 启用对话管理器
    model=bedrock_model,
    system_prompt=SYSTEM_PROMPT
    )
response = agent("My database server: cn-mysql-db-002, ip: 10.25.63.10. There is a CPU usage spike on 2025-05-20, the cpu data is under sample_cases/case-CPU-high-0 folder, please help investigate")
# response = agent("My database server ha a CPU usage spike on 2025-07-14 in case-CPU-high-3, please help investigate")

# Access metrics through the AgentResult
print(f"Total tokens: {response.metrics.accumulated_usage['totalTokens']}")
print(f"Execution time: {sum(response.metrics.cycle_durations):.2f} seconds")
print(f"Tools used: {list(response.metrics.tool_metrics.keys())}")