import click
from .journal import log_entry, search_entries, status_report, clear_entries, edit_entry, delete_entry

@click.group()
def main():
    """Rick MK2 - Personal CLI Assistant"""
    pass

@main.command()
@click.argument("text")
@click.option("--tag", default=None, help="Optional tag for the entry")
def log(text, tag):
    """Log a new journal entry."""
    log_entry(text, tag)
    click.echo(f"✅ Logged entry: '{text}' (tag: {tag})")

@main.command()
@click.option("--text", default=None, help="Search text")
@click.option("--tag", default=None, help="Search tag")
@click.option("--compact", is_flag=True, help="Show compact results")
def search(text, tag, compact):
    """Search journal entries."""
    results = search_entries(text=text, tag=tag)
    if not results:
        click.echo("❌ No matching entries found.")
    else:
        for i, e in enumerate(results, 1):
            if compact:
                click.echo(f"{i}) {e['text']} [{e.get('tag')}]")
            else:
                click.echo(f"{e['timestamp']} [{e.get('tag')}] {e['text']}")

@main.command()
@click.argument("level", default="summary", type=click.Choice(["summary", "full"]))
@click.option("--compact", is_flag=True, help="Show compact results")
def status(level, compact):
    """Show journal status report."""
    report = status_report(level=level)
    click.echo(report["summary"])
    for i, e in enumerate(report["entries"], 1):
        if compact:
            click.echo(f"{i}) {e['text']} [{e.get('tag')}]")
        else:
            click.echo(f"{e['timestamp']} [{e.get('tag')}] {e['text']}")

@main.command()
def clear():
    """Clear all journal entries (with confirmation)."""
    confirm = click.confirm("⚠️ Are you sure you want to clear ALL journal entries?", default=False)
    if confirm:
        msg = clear_entries()
        click.echo(msg)
    else:
        click.echo("❌ Clear cancelled.")

@main.command()
@click.argument("entry_id", type=int)
@click.option("--text", default=None, help="New text for the entry")
@click.option("--tag", default=None, help="New tag for the entry")
def edit(entry_id, text, tag):
    """Edit a journal entry by ID (shows preview)."""
    entries = status_report("full")["entries"]
    if entry_id < 1 or entry_id > len(entries):
        click.echo("❌ Invalid entry ID.")
        return

    entry = entries[entry_id - 1]
    click.echo(f"Preview: {entry_id}) {entry['text']} [{entry.get('tag')}]")

    confirm = click.confirm("✏️ Apply changes to this entry?", default=False)
    if confirm:
        edit_entry(entry_id, text=text, tag=tag)
        click.echo(f"✅ Edited entry {entry_id}.")
    else:
        click.echo("❌ Edit cancelled.")

@main.command()
@click.argument("entry_id", type=int)
def delete(entry_id):
    """Delete a journal entry by ID (shows preview)."""
    entries = status_report("full")["entries"]
    if entry_id < 1 or entry_id > len(entries):
        click.echo("❌ Invalid entry ID.")
        return

    entry = entries[entry_id - 1]
    click.echo(f"Preview: {entry_id}) {entry['text']} [{entry.get('tag')}]")

    confirm = click.confirm(f"⚠️ Delete entry {entry_id}?", default=False)
    if confirm:
        delete_entry(entry_id)
        click.echo(f"🗑️ Deleted entry {entry_id}.")
    else:
        click.echo("❌ Delete cancelled.")
