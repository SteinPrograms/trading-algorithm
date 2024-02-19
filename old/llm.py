import requests
from app.app.helpers.log import logger
from fastapi import HTTPException

def summarizer(content: str) -> str:
    # Create a summary of the article using mistral
    try:
        response = requests.post(
            "http://localhost:8000/summarizer/invoke", json={"input": {"text": content}}
        )
    except Exception:
        logger.error("UNABLE TO CONNECT TO SUMMARIZER API")
        raise HTTPException(
            status_code=404, detail="UNABLE TO CONNECT TO SUMMARIZER API"
        )
    json_response = response.json()
    summary = json_response.get("output")
    return summary



print(summarizer(content="""
Bitcoin’s (BTC) technical fundamentals and use cases have significantly increased in the past year and likely made the asset “stronger” ahead of its historically bullish halving event compared to previous years, crypto asset management Grayscale said in a research note last week.“Despite miner revenue challenges in the short term, fundamental on-chain activity and positive market structure updates make this halving different on a fundamental level,” researcher Michael Zhao said. “While it has long been heralded as digital gold, recent developments suggest that bitcoin is evolving into something even more significant.”Halving is part of the Bitcoin network’s code to reduce inflationary pressure on the cryptocurrency and will cut the rewards in half for successfully mining a bitcoin block. This makes obtaining or mining new bitcoin much harder – and has historically preceded bull runs.Zhao stated that the advent of ordinal inscriptions and BRC-20 tokens had revitalized on-chain activity on Bitcoin, generating upwards of $200 million in transaction fees for miners as of February 2024.“This trend is expected to persist, bolstered by renewed developer interest and ongoing innovations on the Bitcoin blockchain,” he said.The BRC-20 standard (BRC stands for Bitcoin Request for Comment) was introduced in April to allow users to issue transferable tokens directly through the network for the first time.The tokens, called inscriptions, function on the Ordinals Protocol. The protocol allows users to embed data on the Bitcoin blockchain by inscribing references to digital art into small Bitcoin-based transactions.During times of network demand, fees derived from Ordinals they consisted of over 20% of monthly revenue for miners – emerging as a new source of income, one of the network’s most important stakeholders.Beyond generally positive onchain fundamentals, bitcoin’s market structure looks beneficial to price post-halving, the report said. Lower rewards are expected to require relatively lower buying pressure to keep prices afloat, which, with increased demand, could translate to higher prices.“Historically, block rewards have introduced potential sell pressure to the market, with the possibility that all newly mined bitcoin could be sold, impacting prices,” Zhao wrote. “Currently, 6.25 bitcoin mined per block equates to approximately $14 billion annually (assuming bitcoin price is $43K).”“In order to maintain current prices, a corresponding buy pressure of $14 billion annually is needed,” he stated, adding that these requirements will decrease “to $7 billion annually” after the halving as rewards fall down to 3.25 bitcoin per block, “effectively easing the selling pressure.”Spot bitcoin ETFs have amassed more than 192,000 bitcoins in holdings as of Friday since their launch nearly a month ago.The funds have only been on the market for less than one month but have already attracted billions of dollars from investors looking to gain exposure to bitcoin without having to buy and store it directly.
"""))