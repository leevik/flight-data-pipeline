import requests
import json
from datetime import datetime, timedelta, timezone
from src.extract.openskynetwork_token_manager import tokens
import os
from pathlib import Path

#import sys

#print(tokens.headers())
#sys.exit()



now_dt = datetime.now(timezone.utc)
seven_days_ago_dt = now_dt - timedelta(days=1)

now = int(now_dt.timestamp())
seven_days_ago = int(seven_days_ago_dt.timestamp())

OPENSKY_URL = f"https://opensky-network.org/api/flights/departure?airport=EFHK&begin={seven_days_ago}&end={now}"

def fetch_flights():
    response = requests.get(OPENSKY_URL, timeout=30,headers=tokens.headers())
    response.raise_for_status()
    data = response.json()
    return data


def transform(data):
    print("data: ", data)
    records = []

    for flight in data:
        record = {
            "icao24": flight.get("icao24"),
            "callsign": flight.get("callsign").strip() if flight.get("callsign") else None,
            "firstSeen": flight.get("firstSeen"),
            "lastSeen": flight.get("lastSeen"),
            "estDepartureAirport": flight.get("estDepartureAirport"),
            "estArrivalAirport": flight.get("estArrivalAirport"),
            "estDepartureAirportHorizDistance": flight.get("estDepartureAirportHorizDistance"),
            "estDepartureAirportVertDistance": flight.get("estDepartureAirportVertDistance"),
            "estArrivalAirportHorizDistance": flight.get("estArrivalAirportHorizDistance"),
            "estArrivalAirportVertDistance": flight.get("estArrivalAirportVertDistance"),
            "departureAirportCandidatesCount": flight.get("departureAirportCandidatesCount"),
            "arrivalAirportCandidatesCount": flight.get("arrivalAirportCandidatesCount"),
        }
        records.append(record)

    return records


def save_to_file(records):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    folder = Path(os.getenv("LOCAL_DATA_DIR", "/app/data/sample"))
    folder.mkdir(parents=True, exist_ok=True)

    filename = folder / f"flights_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(records, f, indent=2)

    print(f"Saved {len(records)} records to {filename}")


if __name__ == "__main__":
    raw = fetch_flights()
    transformed = transform(raw)
    save_to_file(transformed)