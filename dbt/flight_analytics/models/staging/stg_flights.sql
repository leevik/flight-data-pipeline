SELECT
    f.value:icao24::string AS icao24,
    TRIM(f.value:callsign::string) AS callsign,
    f.value:estDepartureAirport::string AS departure_airport,
    f.value:estArrivalAirport::string AS arrival_airport,
    TO_TIMESTAMP_NTZ(f.value:firstSeen::number) AS first_seen,
    TO_TIMESTAMP_NTZ(f.value:lastSeen::number) AS last_seen,
    DATEDIFF(
        'minute',
        TO_TIMESTAMP_NTZ(f.value:firstSeen::number),
        TO_TIMESTAMP_NTZ(f.value:lastSeen::number)
    ) AS flight_duration_minutes
FROM {{ source('raw', 'flights') }},
LATERAL FLATTEN(input => data) f