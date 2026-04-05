import irsdk
import pandas as pd

def load_ibt(filepath):
    channels = [
        "Lap",
        "LapDistPct",
        "Speed",
        "Throttle",
        "Brake",
        "Lat",
        "Lon"
    ]

    ibt = irsdk.IBT()
    ibt.open(filepath)

    data = {}
    for channel in channels:
        data[channel] = ibt.get_all(channel)

    df = pd.DataFrame(data)
    df = df.rename(columns={"Speed": "SpeedMps"})

    # Convert MPS -> KPH
    df["SpeedKph"] = df["SpeedMps"] * 3.6

    # Convert MPS -> MPH
    df["SpeedMph"] = df["SpeedMps"] * 2.23694

    return df

def get_laps(df):

    lap_dict = {}

    unique_laps = df["Lap"].unique()

    for lap in unique_laps:

        if lap == 0:
            continue

        lap_dict[lap] = df[df["Lap"] == lap]

    return lap_dict

if __name__ == "__main__":
    df = load_ibt("./ibtfiles/test_porschegt4_sonoma.ibt")
    print(f"\ndf: {df.shape}\n")
    print(df.head(10))

    print()

    laps = get_laps(df)
    print(f"Number of laps: {len(laps)}")
    for lap_num, lap_df in laps.items():
        print(f"Lap {lap_num}: {len(lap_df)} samples")
