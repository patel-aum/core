"""
Sphinx extension for ReadTheDocs-style "Edit on GitHub" links on the sidebar.

Loosely based on https://github.com/astropy/astropy/pull/347
"""

import os
import warnings

__licence__ = "BSD (3 clause)"


def get_github_url(app, view, path):
    """Build the GitHub URL."""
    return (
        f"https://github.com/{app.config.edit_on_github_project}/"
        f"{view}/{app.config.edit_on_github_branch}/"
        f"{app.config.edit_on_github_src_path}{path}"
    )


def html_page_context(app, pagename, templatename, context, doctree):
    """Build the HTML page."""
    if templatename != "page.html":
        return

    if not app.config.edit_on_github_project:
        warnings.warn("edit_on_github_project not specified")
        return
    if not doctree:
        warnings.warn("doctree is None")
        return
    path = os.path.relpath(doctree.get("source"), app.builder.srcdir)
    show_url = get_github_url(app, "blob", path)
    edit_url = get_github_url(app, "edit", path)

    context["show_on_github_url"] = show_url
    context["edit_on_github_url"] = edit_url


def setup(app):
    """Set up the app."""
    app.add_config_value("edit_on_github_project", "", True)
    app.add_config_value("edit_on_github_branch", "master", True)
    app.add_config_value("edit_on_github_src_path", "", True)  # 'eg' "docs/"
    app.connect("html-page-context", html_page_context)
