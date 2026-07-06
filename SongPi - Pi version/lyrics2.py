import requests


def get_lyrics(title, artist):
    url = "https://lrclib.net/api/search"

    params = {
        "artist_name": artist,
        "track_name": title
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return []

        data = response.json()

        if not data:
            print("No songs found.")
            return []

        print("Found:", data[0]["trackName"], "-", data[0]["artistName"])

        synced = data[0].get("syncedLyrics")

        if not synced:
            print("No synced lyrics available.")
            return []

        lyrics = []

        for line in synced.split("\n"):

            if "]" not in line:
                continue

            try:
                timestamp, text = line.split("]", 1)
                timestamp = timestamp.replace("[", "")

                mins, rest = timestamp.split(":")
                secs, ms = rest.split(".")

                total_ms = (
                    int(mins) * 60000 +
                    int(secs) * 1000 +
                    int(ms.ljust(3, "0"))
                )

                lyrics.append((total_ms, text.strip()))

            except Exception:
                continue

        return lyrics

    except Exception as e:
        print("Lyrics error:", e)
        return []
