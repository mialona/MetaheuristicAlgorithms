def extensions(features):
    """
    The 'extensions' function calculates the effect of the extensions on the
    features of the machine.

    Args:
        features: Dictionary of machine features and extensions values.

    Returns:
        features: Modified dictionary of machine features and extensions values.
    """

    # Modification of features depending on the extensions
    features["M1_head_A"] = features["M1_head_A"] + features["exten_head_A"]
    features["M2_head_B"] = features["M2_head_B"] - features["exten_head_B"]
    features["M3_collision"] = features["M3_collision"] - features["exten_head_A"] - features["exten_head_B"]

    # Return new features
    return features