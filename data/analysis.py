def generate_insights(lap_a, lap_b, lap_a_time, lap_b_time):
    # Insight 1 - overall time delta
    insights = []
    delta = round(lap_b_time - lap_a_time, 3)

    lap_a_num = lap_a["Lap"].iloc[0]
    lap_b_num = lap_b["Lap"].iloc[0]

    if delta > 0:
        insight1 = f"Lap {lap_a_num} is {delta}s faster than {lap_b_num}"
    elif delta == 0:
        insight1 = f"Lap A and B are the same"
    else:
        insight1 = f"Lap {lap_b_num} is {abs(delta)}s faster than {lap_a_num}"

    insights.append(insight1)

    # Insight 2 - Where most time is lost
    segments = 10
    max_loss = 0
    max_loss_segment = 0

    for i in range(segments):
        start = i / segments
        end = (i+1) / segments

        a_seg = lap_a[(lap_a["LapDistPct"] >= start) & (lap_a["LapDistPct"] <= end)]
        b_seg = lap_b[(lap_b["LapDistPct"] >= start) & (lap_b["LapDistPct"] <= end)]

        if a_seg.empty or b_seg.empty:
            continue

        seg_delta = b_seg["LapDeltaToBestLap"].mean() - a_seg["LapDeltaToBestLap"].mean()

        if abs(seg_delta) > abs(max_loss):
            max_loss = round(seg_delta, 3)
            max_loss_segment = i + 1
        
    seg_start = round((max_loss_segment - 1) / segments, 1)
    seg_end = round(max_loss_segment / segments, 1)
    insight2 = f"Most time difference between Lap {lap_a_num} and Lap {lap_b_num} is in Sector {max_loss_segment} ({seg_start}-{seg_end} of track)"
     
    insights.append(insight2)

    # Insight 3 - Braking consistency

    a_brake_std = round(lap_a["Brake"].std(), 3)
    b_brake_std = round(lap_b["Brake"].std(), 3)

    brake_delta = round(b_brake_std - a_brake_std, 3)

    # b-a > 0 means b is less consistent
    if brake_delta > 0:
        insight3 = f"Lap {lap_a_num} has more consistent braking than Lap {lap_b_num} (std: {a_brake_std} vs {b_brake_std})"
    # b-a = 0 means equal consistency
    elif brake_delta == 0:
        insight3 = f"Lap {lap_a_num} and Lap {lap_b_num} have equal braking consistency"
    # b-a < 0 means b is more consistent
    else:
        insight3 = f"Lap {lap_b_num} has more consistent braking than Lap {lap_a_num} (std: {b_brake_std} vs {a_brake_std})"

    insights.append(insight3)
    return insights