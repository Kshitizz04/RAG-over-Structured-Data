import io
import matplotlib.pyplot as plt
import pandas as pd

def generate_chart(
    df: pd.DataFrame,
    chart_type: str,
    x_col: str,
    y_col: str,
    color: str = "#007acc",
    marker: str = "o"
):
    # Validate columns
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(f"Invalid columns: {x_col}, {y_col}")

    # Drop NA for plotting
    plot_df = df[[x_col, y_col]].dropna()

    plt.figure(figsize=(8, 5))

    # Detect categorical x-axis for bar charts
    is_x_categorical = pd.api.types.is_object_dtype(plot_df[x_col]) or pd.api.types.is_categorical_dtype(plot_df[x_col])

    if chart_type.lower() == "line":
        plt.plot(plot_df[x_col], plot_df[y_col], marker=marker, color=color)
    elif chart_type.lower() == "bar":
        if is_x_categorical:
            plt.bar(plot_df[x_col].astype(str), plot_df[y_col], color=color)
            plt.xticks(rotation=45, ha="right")
        else:
            plt.bar(plot_df[x_col], plot_df[y_col], color=color)
    elif chart_type.lower() == "scatter":
        plt.scatter(plot_df[x_col], plot_df[y_col], color=color, marker=marker)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{chart_type.title()} Chart: {y_col} vs {x_col}")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()

    description = f"{chart_type.title()} chart of '{y_col}' vs '{x_col}'"
    return buf, description
