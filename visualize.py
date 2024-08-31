import curses
import shutil
from rich.console import Console, Group
from rich.table import Table
from rich.text import Text
from rich.progress import Progress
from rich.layout import Layout
from rich.panel import Panel
from rich import box
from term_piechart import Pie
from rich.padding import Padding
from rich.live import Live

console = Console()

def plot_pie_chart(data, title="Pie Chart"):
    data = [{"name": k, "value": v} for k, v in data.items()]
    pie = Pie(
        data,
        radius=7,
        autocolor=True,
        autocolor_pastel_factor=0.7,
        legend={"line": 0, "format": "{label} {name:<8} {percent:>5.2f}% [{value}]"},
    )
    text = Text.from_ansi(pie.render())
    return Panel(text, title=title)

def show_progress_bar(value, total, label):
    progress = Progress()
    task = progress.add_task(label, total=total)
    progress.update(task, advance=value)
    return progress.get_renderable()

def visualize_project(layout, project_name, stats):
    panel = Panel(f"[bold cyan]Project: {project_name}[/bold cyan]")
    
    layout.split_column(Layout(panel, name="heading"), Layout(name="main"))
    layout["heading"].size = 3
    layout["main"].split_column(Layout(name="upper"), Layout(name="lower"), Layout(name="footer"))
    layout["main"]["upper"].split_row(Layout(name="left"), Layout(name="right"))

    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
    table.add_column("Metric", justify="right")
    table.add_column("Value", justify="right")

    table.add_row("Total Files", str(stats["total_files"]))
    table.add_row("Total Lines", str(stats["total_lines"]))
    table.add_row("Total Blanks", str(stats["total_blanks"]))
    table.add_row("Total Comments", str(stats["total_comments"]))
    table.add_row("Lines of Code", str(stats["total_lines_of_code"]))
    table.add_row("Boilerplate Lines", str(stats["boilerplate_lines"]))
    table.add_row("Actual Code Lines", str(stats["actual_code_lines"]))
    layout["main"]["upper"]["left"].update(Panel(table))

    progress_panel = Panel.fit(Group(
        show_progress_bar(stats["actual_code_lines"], stats["total_lines"], "Actual Code Lines"),
        show_progress_bar(stats["boilerplate_lines"], stats["total_lines"], "Boilerplate Lines"),
        show_progress_bar(stats["total_comments"], stats["total_lines"], "Comment Lines"),
        show_progress_bar(stats["total_blanks"], stats["total_lines"], "Blank Lines"))
    )
    layout["main"]["lower"].add_split(progress_panel)

    pie_chart_panel = Panel(plot_pie_chart(stats["language_distribution"]), title="Language Distribution")
    layout["main"]["upper"]["right"].update(pie_chart_panel)

    actual_code_percentage = (stats["actual_code_lines"] / stats["total_lines"]) * 100
    rank = ""
    if actual_code_percentage > 75:
        rank = "[bold green]Excellent[/bold green]"
    elif actual_code_percentage > 50:
        rank = "[bold yellow]Good[/bold yellow]"
    else:
        rank = "[bold red]Needs Improvement[/bold red]"

    rank_panel = Panel.fit(f"Rank: {rank}")
    layout["main"]["footer"].add_split(rank_panel)

    layout["main"]["upper"].size = 20
    layout["main"]["lower"].size = 6
    layout["main"]["footer"].size = 3


def visualize_data(data):
    # projects = list(data.items())
    # index = 0

    # def display_screen(stdscr):
    #     nonlocal index
    #     curses.curs_set(0)  # Hide cursor
    #     stdscr.nodelay(True)

    #     with Live(console=console, refresh_per_second=4, redirect_stdout=True, vertical_overflow="ellipsis") as live:
    #         layout = Layout()
    #         project_name, stats = projects[index]
    #         visualize_project(layout, project_name, stats)
    #         console.print(layout)

    #         while True:
    #             key = stdscr.getch()
    #             if key == curses.KEY_LEFT:
    #                 index = max(0, index - 1)
    #                 project_name, stats = projects[index]
    #                 layout = Layout()
    #                 visualize_project(layout, project_name, stats)
    #                 console.print(layout)
    #             elif key == curses.KEY_RIGHT:
    #                 index = min(len(projects) - 1, index + 1)
    #                 project_name, stats = projects[index]
    #                 layout = Layout()
    #                 visualize_project(layout, project_name, stats)
    #                 console.print(layout)
    #             elif key == ord("q"):
    #                 break

    # live screen not working so simplifying

    with Live(console=console) as live:
        for project_name, stats in data.items():
            layout = Layout()
            visualize_project(layout, project_name, stats)
            _width, _height = shutil.get_terminal_size()
            console.size = (_width-1, _height-4)
            console.print(layout)
            input("Press Enter to continue...")
            console.clear()

    # curses.wrapper(display_screen)