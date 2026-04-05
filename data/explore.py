import irsdk
import pandas as pd

ibt = irsdk.IBT()
filename = "test_porschegt4_sonoma.ibt"
ibt.open(f"./ibtfiles/{filename}")


speeds = ibt.get_all("Lap")
speeds = ibt.get_all("Speed")
throttle = ibt.get_all("Throttle")
brake = ibt.get_all("Brake")
lap = ibt.get_all("Lap")
lap_dist = ibt.get_all("LapDistPct")
lat = ibt.get_all("Lat")
lon = ibt.get_all("Lon")

df = pd.DataFrame({
    "Lap": lap,
    "SpeedMps": speeds,
    "Throttle": throttle,
    "Brake": brake,
    "Lap": lap,
    "LapDistPct": lap_dist,
    "Lat": lat,
    "Lon": lon
})

# Convert MPS -> KPH
df["SpeedKph"] = df["SpeedMps"] * 3.6

# Convert MPS -> MPH
df["SpeedMph"] = df["SpeedMps"] * 2.23694


print()
print(ibt.var_headers_names)
print(f"\ndf: {df.shape}\n")
df = df[df['Lap'] == 1]
print(df.head(10))



