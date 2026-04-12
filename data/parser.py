import irsdk
import pandas as pd

CHANNELS = [
    "Lap",
    "Speed",
    "Throttle",
    "Brake",
    "LapDistPct",
    "Lat",
    "Lon",
    "LapDeltaToBestLap",
    "LapCurrentLapTime",
    "LapBestLapTime",
    "LapLastLapTime",
    "OnPitRoad",
]

def load_ibt(filepath):
    ibt = irsdk.IBT()
    ibt.open(filepath)
    data = {}
    for channel in CHANNELS:
        data[channel] = ibt.get_all(channel)
    df = pd.DataFrame(data)
    df = df.rename(columns={"Speed": "SpeedMps"})
    df["SpeedKph"] = df["SpeedMps"] * 3.6
    df["SpeedMph"] = df["SpeedMps"] * 2.23694
    return df

def get_laps(df):
    lap_dict = {}
    unique_laps = df["Lap"].unique()
    for lap in unique_laps:
        if lap == 0 or lap == 1:
            continue
        lap_df = df[df["Lap"] == lap]
        if lap_df["OnPitRoad"].any():
            continue
        lap_dict[int(lap)] = lap_df
    return lap_dict

def get_lap_time(df, lap_num):
    next_lap = df[df["Lap"] == lap_num + 1]
    if next_lap.empty:
        return 0
    non_zero = next_lap[next_lap["LapLastLapTime"] > 0]
    if non_zero.empty:
        return 0
    return non_zero["LapLastLapTime"].iloc[0]

# Old version
# def get_corners(lap_df, min_speed_threshold=0.85, min_distance=0.03):
#     max_speed = lap_df["SpeedMph"].max()
#     threshold = max_speed * min_speed_threshold
#     corners = []
#     last_corner_dist = -min_distance
#     in_corner = False
#     corner_start = None

#     for _, row in lap_df.iterrows():
#         if row["SpeedMph"] < threshold:
#             if not in_corner:
#                 in_corner = True
#                 corner_start = row["LapDistPct"]
#             corner_end = row["LapDistPct"]
#         else:
#             if in_corner:
#                 mid = (corner_start + corner_end) / 2
#                 if mid - last_corner_dist >= min_distance:
#                     corners.append((corner_start, corner_end))
#                     last_corner_dist = mid
#                 in_corner = False

#     return corners

# def get_corners(lap_df, min_distance=0.025):
#     import numpy as np
#     from scipy.signal import find_peaks

#     speeds = lap_df["SpeedMph"].values
#     dist = lap_df["LapDistPct"].values

#     # Find local minima by inverting the speed signal
#     minima_idx, _ = find_peaks(-speeds, distance=int(len(speeds) * min_distance))

#     corners = []
#     for idx in minima_idx:
#         center = dist[idx]
#         start = max(0, center - 0.02)
#         end = min(1.0, center + 0.02)
#         min_speed = speeds[idx]
#         if min_speed < 100:  # ignore high speed false detections
#             corners.append((start, end))

#     return corners

# def get_corner_summary(lap_a, lap_b, corners):
#     rows = []
#     for i, (start, end) in enumerate(corners):
#         a_corner = lap_a[(lap_a["LapDistPct"] >= start) & (lap_a["LapDistPct"] <= end)]
#         b_corner = lap_b[(lap_b["LapDistPct"] >= start) & (lap_b["LapDistPct"] <= end)]

#         if a_corner.empty or b_corner.empty:
#             continue

#         a_min_speed = round(a_corner["SpeedMph"].min(), 1)
#         b_min_speed = round(b_corner["SpeedMph"].min(), 1)
#         speed_delta = round(b_min_speed - a_min_speed, 1)

#         a_brake_start = a_corner[a_corner["Brake"] > 0.05]["LapDistPct"].min()
#         b_brake_start = b_corner[b_corner["Brake"] > 0.05]["LapDistPct"].min()
#         brake_delta = round((b_brake_start - a_brake_start) * 100, 3) if not (
#             pd.isna(a_brake_start) or pd.isna(b_brake_start)) else 0

#         rows.append({
#             "Corner": f"T{i+1}",
#             "Min Speed A": a_min_speed,
#             "Min Speed B": b_min_speed,
#             "Speed Δ": speed_delta,
#             "Brake Δ (%)": brake_delta,
#         })

#     return pd.DataFrame(rows)

if __name__ == "__main__":

    ibt = irsdk.IBT()
    ibt.open("./ibtfiles/test_porschegt4_sonoma.ibt")
    print(dir(ibt))
    print(ibt._IBT__session_info_dict.keys())

    df = load_ibt("./ibtfiles/test_porschegt4_sonoma.ibt")
    print(f"\ndf: {df.shape}\n")
    laps = get_laps(df)
    lap = laps[2]
    
    corners = get_corners(lap)
    print(f"Found {len(corners)} corners:")
    for i, (start, end) in enumerate(corners):
        corner_data = lap[(lap["LapDistPct"] >= start) & (lap["LapDistPct"] <= end)]
        min_speed = corner_data["SpeedMph"].min()
        print(f"T{i+1}: {start:.3f} - {end:.3f} | min speed: {min_speed:.1f} mph")


    # Lap Debugging
    # print(f"Number of laps: {len(laps)}")
    # for lap_num, lap_df in laps.items():
    #     print(f"Lap {lap_num}: {len(lap_df)} samples — {get_lap_time(df, lap_num)}s")