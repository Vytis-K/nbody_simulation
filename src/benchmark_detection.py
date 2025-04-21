import json
import numpy as np
import pandas as pd
from pathlib import Path

from astropy.timeseries import BoxLeastSquares
from transitleastsquares import transitleastsquares


def run_bls(time, flux, min_period=0.5, max_period=None, n_periods=5000):
    """
    Run Box Least Squares on (time_days, flux).
    - periods: from min_period to max_period (default half the baseline)
    - durations: 1%–20% of the MINIMUM period (so they always satisfy duration < period)
    Returns the best period, duration, T0, depth, and power.
    """
    if max_period is None:
        max_period = (time.max() - time.min()) / 2

    # 1) define trial periods
    periods = np.linspace(min_period, max_period, n_periods)

    # 2) define durations as fractions of the smallest period
    #    so max(durations) = 0.2 * min_period < min_period
    dur_min = 0.01 * min_period
    dur_max = 0.20 * min_period
    durations = np.linspace(dur_min, dur_max, 20)

    # 3) run BLS
    bls = BoxLeastSquares(time, flux)
    bls_power = bls.power(periods, durations)

    # 4) pick the best period
    idx = np.argmax(bls_power.power)

    return {
        "period":   float(bls_power.period[idx]),
        "duration": float(bls_power.duration[idx]),
        "t0":       float(bls_power.transit_time[idx]),
        "depth":    float(bls_power.depth[idx]),
        "power":    float(bls_power.power[idx])
    }



def run_tls(time, flux):
    """
    Run Transit Least Squares on (time_days, flux).
    Returns period, duration, T0, depth, and SNR.
    If TLS fails (e.g. empty arrays), returns None for all fields
    and logs the error in an "error" key.
    """
    try:
        model = transitleastsquares(time, flux)
        res   = model.power()
        return {
            "period":   float(res.period),
            "duration": float(res.duration),
            "t0":       float(res.T0),
            "depth":    float(res.depth),
            "snr":      float(res.snr),
            "error":    None
        }
    except Exception as e:
        print(f"⚠️  TLS failed on this curve: {e}")
        return {
            "period":   None,
            "duration": None,
            "t0":       None,
            "depth":    None,
            "snr":      None,
            "error":    str(e)
        }



def benchmark_lightcurves(
    curves_dir: str = "data/lightcurves",
    output_file: str = "data/benchmark_results.json"
):
    """
    For each lc_*.csv in curves_dir:
      1. Load time (s) & flux_noisy,
      2. Convert time → days,
      3. Run BLS & TLS,
      4. Load events_*.json for truth,
      5. Estimate true_period if ≥2 events,
      6. Flag missed_transits & wrong_periodicity,
      7. Write summary to output_file.
    """
    results = []
    curves_path = Path(curves_dir)

    for lc_path in sorted(curves_path.glob("lc_*.csv")):
        idx = int(lc_path.stem.split("_")[1])
        df = pd.read_csv(lc_path)

        # time in seconds → days
        time_s = df["time"].values
        time   = time_s / 86400.0
        flux   = df["flux_noisy"].values

        # run classical detectors
        bls_res = run_bls(time, flux)
        tls_res = run_tls(time, flux)

        # load ground-truth events
        events_path = curves_path / f"events_{idx}.json"
        if events_path.exists():
            with open(events_path) as f:
                truth_events = json.load(f)
        else:
            truth_events = []

        # estimate true period (days) if we have ≥2 events
        if len(truth_events) >= 2:
            start_times = np.array([e["start_time"] for e in truth_events]) / 86400.0
            true_period = float(np.median(np.diff(start_times)))
        else:
            true_period = None

        # define simple failure flags
        missed = len(truth_events) > 0 and bls_res["power"] < 1.0
        wrong_period = (
            True if true_period
            and abs(bls_res["period"] - true_period) > 0.1 * true_period
            else False
        ) if true_period else None

        results.append({
            "index": idx,
            "n_truth_events": len(truth_events),
            "true_period":    true_period,
            "bls":            bls_res,
            "tls":            tls_res,
            "failure": {
                "missed_transits":    missed,
                "wrong_periodicity":  wrong_period
            }
        })

    # write summary JSON
    out_path = Path(output_file)
    out_path.parent.mkdir(exist_ok=True, parents=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Benchmark complete. Results -> {out_path}")
    return results


if __name__ == "__main__":
    benchmark_lightcurves()
