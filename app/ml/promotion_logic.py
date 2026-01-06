EPSILON = 0.01  # tolerance

def should_promote(new_metrics, prod_metrics, new_config, prod_config):
    # 🔴 Block identical configs immediately
    if prod_config is not None and new_config == prod_config:
        return False

    if prod_metrics is None:
        return True  # first model ever

    gen_improved = (
        new_metrics["avg_generation_score"]
        > prod_metrics["avg_generation_score"] + EPSILON
    )

    latency_improved = (
        new_metrics["avg_latency"]
        < prod_metrics["avg_latency"] - EPSILON
    )

    return gen_improved or latency_improved
