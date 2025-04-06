**TORY - Token Unlock Analyst Agent**

This agent receives token unlock event data and uses AI to provide structured insights about the impact of those unlocks.

It accepts a message with:
- `uuid`: A unique string identifier for tracking the request.
- `timestamp`: The UNIX timestamp when the request was created.
- `token`: a token unlock stringify JSON format

The response sent back includes:
- `uuid`: Same ID from request.
- `timestamp`: Same timestamp from request.
- `summary`: AI-generated JSON string containing `"bullishThoughts"` and `"bearishThoughts"` arrays.

### Example Request
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": 1712428800,
  "payload": "[{\"date\":\"2025-03-15T00:00:00.000Z\",\"totalUnlockedTokens\":63990287,\"percentOfSupplyUnlocked\":0.0063990287,\"categories\":[{\"name\":\"Early Contributors\",\"unlockedTokens\":33560988,\"percentUnlocked\":1.6747},{\"name\":\"Investors\",\"unlockedTokens\":30429299.000000004,\"percentUnlocked\":1.6747}],\"metrics\":{\"price\":{\"sevenDaysBefore\":0.183992,\"at\":0.175539,\"sevenDaysAfter\":0.161529},\"volume\":{\"sevenDaysBefore\":44327129,\"at\":25089796,\"sevenDaysAfter\":29090782},\"openInterest\":{\"sevenDaysBefore\":23161711.698561043,\"at\":29081035.06212187,\"sevenDaysAfter\":29908152.10476917},\"fundingRate\":{\"sevenDaysBefore\":-0.009168623650614998,\"at\":-0.019051154420385002,\"sevenDaysAfter\":-0.0006347076973233332},\"social\":{\"interactions\":{\"sevenDaysBefore\":38905,\"at\":38905,\"sevenDaysAfter\":38905},\"creators\":{\"sevenDaysBefore\":275,\"at\":275,\"sevenDaysAfter\":275}}}},...]"
}
```

### Example Response
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": 1712428800,
  "summary": "{\"bullishThoughts\":[\"Open interest increased by 24% after Nov unlock...\"],\"bearishThoughts\":[\"4 out of 6 past unlocks saw price drop within 7 days...\"]}"
}
```