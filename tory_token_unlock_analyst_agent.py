from uagents import Agent, Context, Protocol, Model
import requests

# Define request and response models
class UnlocksRequest(Model):
    uuid: str
    timestamp: int
    token: str

class UnlocksResponse(Model):
    uuid: str
    timestamp: int
    summary: str

# Instantiate the agent
unlocks_agent = Agent(
  name="unlocks_agent",
  seed="SECRET_SEED"
)

# Create a protocol instance
unlocks_protocol = Protocol("UnlocksProtocol")

# Message handler
@unlocks_protocol.on_message(model=UnlocksRequest)
async def handle_unlocks_request(ctx: Context, sender: str, msg: UnlocksRequest):
    ctx.logger.info(f"[UnlocksAgent] ✅ Received Unlocks Request: {msg.uuid} at {msg.timestamp}")

    # Prepare ASI Completion API payload
    request_data = {
        "model": "asi1-mini",
        "temperature": 0,
        "stream": False,
        "max_tokens": 10000,
        "messages": [
            {
                "role": "system",
                "content": "You are a crypto tokenomics analyst. Analyze token unlock events with the goal of forming future expectations from past behavior.\n\nUse this logic:\n- Examine the percentage of supply unlocked and whether it’s higher or lower than previous unlocks.\n- Track which categories are unlocking and whether they’ve historically correlated with post-unlock price moves (e.g., strategic/private round allocations).\n- Consider price/volume/open interest/funding rate trends before and after previous unlocks and identify repeatable patterns.\n- Look at consistency or changes in social metrics like interactions or contributors.\n- If price/volume/interest patterns frequently repeat after similar unlock types, highlight those as predictive indicators.\n\nOnly return a valid single-line JSON object in this format: {\"bullishThoughts\":[\"...\"],\"bearishThoughts\":[\"...\"]}.\n\nRequirements:\n- All thoughts must include measurable, quantitative logic (e.g., % unlocked, price delta, open interest change).\n- Avoid vague opinions like “this looks good” or “the team is strong”.\n- Each section (bullish/bearish) must include AT LEAST 3 bullet points.\n- Focus on **what past patterns suggest about potential future outcomes**.\n- Do NOT include markdown, extra explanation, or natural language — return a raw JSON object only.\n\nDo NOT wrap your response in code blocks like ```json. Only return raw valid JSON without any prefix or suffix."
            }
            ,
            {"role": "user", "content": "Please analyze the following token unlock and metric data:"},
            {"role": "user", "content": msg.token}
        ]
    }

    try:
        ctx.logger.info("🌐 Calling ASI unlock analysis API...")
        response = requests.post(
            url='https://api.asi1.ai/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY'
            },
            json=request_data
        )
        response.raise_for_status()
        result = response.json()
        summary = result['choices'][0]['message']['content']
        ctx.logger.info("✅ Unlocks response received.")
    except Exception as e:
        ctx.logger.error(f"❌ Unlocks analysis failed: {e}")
        summary = "Unlock analysis unavailable."

    # Send response back
    ctx.logger.info("📤 Sending UnlocksResponse back to coordinator...")
    await ctx.send(sender, UnlocksResponse(
        uuid=msg.uuid,
        timestamp=msg.timestamp,
        summary=summary
    ))

# Register protocol
unlocks_agent.include(unlocks_protocol)

# Run agent
if __name__ == "__main__":
    unlocks_agent.run()
