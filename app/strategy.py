def generate_signal(
    trend,
    sweep_structure,
    entry_zone
):

    if trend == "DOWN":

        if sweep_structure["event"] == "CHoCH":

            if sweep_structure["direction"] == "BEARISH":

                return {
                    "signal": "SHORT",
                    "entry_zone": entry_zone,
                    "confidence": 80
                }


    return None