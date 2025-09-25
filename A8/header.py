
from __future__ import annotations
from datetime import datetime
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

# Internal mapping from task number to task name.
# Edit/extend as needed.
TASK_NAMES = {
    0: "Studium spekter záření gama polovodičovým\nspektrometrem.",
    1: "Objevování částic v detektoru ATLAS v CERN.",
    2: "Studium plynových detektorů.",
    3: "Identifikace prvků na základě jejich charakteristického\nrentgenového záření.",
    4: "Totální účinný průřez interakce gama záření -\nabsorpční koeficient záření gama pro některé elementy.",
    5: "Spektrometrie záření alpha",
    6: "Simulace průchodu částic hadronovým kalorimetrem.",
    7: "Pozitronová emisní tomografie.",
    8: "Absorpce beta záření.",
}

def _cz_date_string(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y")

def header(*, student: str, task_no: int, date: str | None = None, task_name: str | None = None, show: bool = True):
    """
    Draw an introductory page for 'Fyzikální praktikum' resembling the provided template.

    Parameters
    ----------
    student : str
        Student's full name.
    task_no : int
        Task number (Úloha č.).
    date : str | None, optional
        Measurement date in format 'DD.MM.YYYY'. If None, uses today's date in Europe/Prague timezone.
    task_name : str | None, optional
        Task name. If None, will try to look up via TASK_NAMES; if not found, leaves a blank line.
    show : bool, default True
        Whether to display the figure via plt.show(). The function returns (fig, ax).
    """
    # Resolve date
    if date is None or str(date).strip() == "":
        date_str = _cz_date_string(datetime.now(ZoneInfo("Europe/Prague")))
    else:
        date_str = date

    # Resolve task name
    resolved_task_name = task_name if (task_name and str(task_name).strip()) else TASK_NAMES.get(task_no, "")

    # Figure setup: A4 portrait proportions
    fig = plt.figure(figsize=(8.27, 11.69), dpi=150)  # A4 portrait
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Margins
    left = 0.08
    right = 0.92
    top = 0.95
    line_h = 0.028  # line height

    # Large rectangle around the header
    header_top = top + 0.8*line_h
    header_height = 0.32
    rect = Rectangle((left-0.05, header_top - header_height), right - left + 0.1, header_height,
                     fill=False, linewidth=1)
    ax.add_patch(rect)

    # Header texts
        # Header texts (top-left)
    ax.text(left, top, "Kabinet výuky obecné fyziky, UK MFF", ha="left", va="top", fontsize=12)
    ax.text(left, top - 1.2*line_h, f"Fyzikální praktikum 4", ha="left", va="top", fontsize=16, fontweight="bold")

    # Logo in top-right
    try:
        logo_img = mpimg.imread(r"logo_zfp.png")
        ax.imshow(logo_img, extent=(0.73, right, top-3*line_h, top-0.2*line_h), aspect="auto", zorder=5)
    except Exception as e:
        print("Could not load logo:", e)


    y = top - 4*line_h

    # "Úloha č." with dotted line
    ax.text(left, y, "Úloha č.", ha="left", va="center", fontsize=13)
    # number
    ax.text(left+0.18, y, f"{task_no}", ha="left", va="center", fontsize=13)

    y -= 1.8*line_h
    # "Název úlohy:"
    ax.text(left, y, "Název úlohy:", ha="left", va="center", fontsize=13)
    if resolved_task_name:
        ax.text(left+0.18, y, resolved_task_name, ha="left", va="center", fontsize=13)

    y -= 1.8*line_h
    # "Jméno:"
    ax.text(left, y, "Jméno:", ha="left", va="center", fontsize=13)
    ax.text(left+0.18, y, student, ha="left", va="center", fontsize=13)

    y -= 1.8*line_h
    # "Datum měření:"
    ax.text(left, y, "Datum měření:", ha="left", va="center", fontsize=13)
    ax.text(left+0.18, y, date_str, ha="left", va="center", fontsize=13)

    # Comments box
    y -= 2.2*line_h
    ax.text(left, y, "Připomínky opravujícího:", ha="left", va="center", fontsize=13)
    # Large rectangle for comments
    comments_top = y - 0.8*line_h
    comments_height = 0.22
    rect = Rectangle((left, comments_top - comments_height), right - left, comments_height,
                     fill=False, linewidth=0)
    ax.add_patch(rect)

    # Scoring table header
    table_top = comments_top - comments_height - 2.0*line_h
    ax.text(left, table_top, "", ha="left", va="center", fontsize=12)
    ax.text(right, table_top, "Udělený počet bodů", ha="right", va="center", fontsize=12)

    # Table rows
    rows = [
        #("Teoretická část", "0 - 2"),
        ("Výsledky a zpracování měření", ""),
        ("Diskuse výsledků", ""),
        ("Závěr", ""),
        ("Seznam použité literatury", ""),
        ("Celkem", "max. 12"),
    ]

    yrow = table_top - 1.4*line_h
    row_gap = 1.25*line_h

    # Vertical separator between labels and points
    sep_x = left + 0.55*(right - left)

    # Draw horizontal baseline for the table (subtle guides)
    for i, (label, pts) in enumerate(rows):
        ax.text(left, yrow, label, ha="left", va="center", fontsize=12)
        ax.text(sep_x - 0.02, yrow, pts, ha="right", va="center", fontsize=12)
        # line for awarded points on right
        ax.plot([sep_x+0.02, right], [yrow, yrow], linestyle=(0, (2, 2)), linewidth=1, color='black')
        yrow -= row_gap

    # "Posuzoval" line at the bottom
    bottom_y = yrow - 1.2*row_gap
    ax.text(left, bottom_y, "Posuzoval:", ha="left", va="center", fontsize=12)
    ax.plot([left+0.16, left+0.52], [bottom_y, bottom_y], linestyle=(0, (2, 2)), linewidth=1, color='black')

    ax.text(left+0.60, bottom_y, "dne:", ha="left", va="center", fontsize=12)
    ax.plot([left+0.70, right], [bottom_y, bottom_y], linestyle=(0, (2, 2)), linewidth=1, color='black')

    

    if show:
        plt.show()

    return fig, ax
