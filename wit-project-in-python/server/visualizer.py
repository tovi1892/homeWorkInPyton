import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_histogram(ax, functions: list):
    """גרף 1: היסטוגרמה - התפלגות אורכי פונקציות"""
    lengths = [func["length"] for func in functions]
    if lengths:
        ax.hist(lengths, bins=range(1, max(lengths) + 5, 2), color='skyblue', edgecolor='black')
    else:
        ax.text(0.5, 0.5, 'No functions found', ha='center', va='center', fontsize=12)

    ax.set_title("Distribution of Function Lengths")
    ax.set_xlabel("Function Length (Lines)")
    ax.set_ylabel("Number of Functions")
    ax.grid(axis='y', linestyle='--', alpha=0.7)


def plot_pie_chart(ax, issues_summary: dict):
    """גרף 2: דיאגרמת עוגה - שגיאות לפי סוג בעיה"""
    filtered_issues = {k: v for k, v in issues_summary.items() if v > 0}
    if filtered_issues:
        labels = list(filtered_issues.keys())
        sizes = list(filtered_issues.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
               colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    else:
        ax.text(0.5, 0.5, 'Excellent Code!\n0 Issues Found', ha='center', va='center', fontsize=12, color='green')
        ax.axis('off')

    ax.set_title("Issues Distribution by Type")


def plot_bar_chart(ax, filename: str, issues_summary: dict):
    """גרף 3: גרף עמודות - כמות שגיאות לפי קובץ"""
    total_issues = sum(issues_summary.values())
    ax.bar([filename], [total_issues], color='salmon', edgecolor='black', width=0.4)

    ax.set_title("Number of Issues per File")
    ax.set_xlabel("Files")
    ax.set_ylabel("Number of Issues")
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)



def generate_three_graphs_report(filename: str, functions: list, issues_summary: dict) -> io.BytesIO:
    """
    פונקציה רביעית מנהלת: מייצרת לוח ציור אחד, קוראת לשלוש פונקציות הציור,
    ושומרת את התוצאה המאוחדת לזיכרון ה-RAM.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

    plot_histogram(ax1, functions)
    plot_pie_chart(ax2, issues_summary)
    plot_bar_chart(ax3, filename, issues_summary)
    plt.tight_layout()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    plt.close(fig)

    return img_buf