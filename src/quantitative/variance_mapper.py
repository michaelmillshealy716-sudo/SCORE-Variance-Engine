import numpy as np

def map_gaussian_variance(pure_signal, current_value):
    """
    SCORE: Gaussian Variance Execution
    Calculates the standard deviations (Z-score) from the mean.
    f(x) = (1 / sigma*sqrt(2pi)) * e^(-0.5 * ((x - mu) / sigma)^2)
    """
    mu = np.mean(pure_signal)
    sigma = np.std(pure_signal)

    if sigma == 0:
        return 0.0

    z_score = (current_value - mu) / sigma

    print("\n--- SCORE: 24K Gaussian Variance Analysis ---")
    print(f"Mean (μ): {mu:.2f} | Std Dev (σ): {sigma:.2f}")
    print(f"Current Value Z-Score: {z_score:.2f}σ")

    if z_score <= -2.5:
        print("[EXECUTE] -2.5σ deviation detected. High-conviction Buy the Dip.")
    elif z_score >= 2.5:
        print("[EXECUTE] +2.5σ deviation detected. Overextended, trigger profit-taking.")

    return z_score

def map_logarithmic_growth(price_series):
    """
    SCORE: Natural Logarithmic Trend Analysis
    Models sustained, compounding bull trends using natural log returns.
    ln(P_t / P_t-1)
    """
    if len(price_series) < 2:
        return 0.0

    # Calculate log returns to measure organic compounding velocity
    log_returns = np.diff(np.log(price_series))
    trend_velocity = np.mean(log_returns)

    print("\n--- SCORE: Logarithmic Trend Velocity ---")
    print(f"Piston Velocity: {trend_velocity:.6f}")

    if trend_velocity > 0.001:
        print("Status: Sustained compounding growth. Hold frame.")
    elif trend_velocity < 0:
        print("Status: Growth decelerating. Prepare for variance shift.")

    return trend_velocity

