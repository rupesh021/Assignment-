from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import requests

app = FastAPI()

def calculate_net_profit(scheme_code, start_date, end_date, capital):
    
    start_date = datetime.strptime(start_date, "%d-%m-%Y")
    
    end_date = datetime.strptime(end_date, "%d-%m-%Y")
    
    api_url = f"https://api.mfapi.in/mf/{scheme_code}"
    
    response = requests.get(api_url)
    
    data = response.json()

    available_dates = [entry["date"] for entry in data["data"]]
    
    start_date = next((date for date in sorted(available_dates) if date >= start_date.strftime("%d-%m-%Y")), available_dates[0])
    
    end_date = next((date for date in sorted(available_dates) if date >= end_date.strftime("%d-%m-%Y")), available_dates[-1])

    initial_investment = capital
    
    redemption_value = next(entry["nav"] for entry in data["data"] if entry["date"] == end_date)
    
    net_profit = redemption_value - initial_investment

    return net_profit

@app.get("/profit")
def get_profit(scheme_code: str, start_date: str, end_date: str, capital: float):
    try:
        net_profit = calculate_net_profit(scheme_code, start_date, end_date, capital)
        return {"net_profit": net_profit}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        