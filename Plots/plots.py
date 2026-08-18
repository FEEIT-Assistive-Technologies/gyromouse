import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV file into a pandas DataFrame
df = pd.read_csv("./teleplot_2026-6-23_16-13.csv")

# 2. Create the line plot
# Specify which columns to use for the X and Y axes
plt.plot(
    df["timestamp(ms)"].interpolate(method="linear"),
    df["varx"].interpolate(method="linear"),
    marker=".",
    color="b",
    linestyle="-",
    label="Mouse X axis",
)
plt.plot(
    df["timestamp(ms)"].interpolate(method="linear"),
    df["vary"].interpolate(method="linear"),
    marker=".",
    color="r",
    linestyle="-",
    label="Mouse Y axis",
)


# Highlight specific background regions based on X values
plt.axvspan(
    1782223962, 1782223964.5, facecolor="red", alpha=0.2, label="Vertical movement"
)
plt.axvspan(
    1782223964.5,
    1782223966.5,
    facecolor="yellow",
    alpha=0.2,
    label="Horisontal movement",
)
plt.axvspan(
    1782223966.5, 1782223971, facecolor="green", alpha=0.2, label="Diagonal movement"
)

# 3. Add titles and labels for clarity
plt.title("Mouse cursor movement", fontsize=20)
plt.xlabel("Time [seconds]", fontsize=18)
plt.ylabel("Relative movment from current position [pixels]", fontsize=18)

# 4. Enhance the visual layout
plt.grid(True)
plt.tight_layout()
plt.xlim(left=1782223961, right=1782223971.6)
plt.legend(loc="lower left")
plt.legend(fontsize=18)

# 5. Display the plot
plt.show()

plt.show()

print("done")
