"""
About Project Blueprint
Provides academic project background, system architecture flow, technology explanations,
and viva viva presentation summary.
"""

from flask import Blueprint, render_template

about_bp = Blueprint("about", __name__)

@about_bp.route("/about")
def about_view():
    """Renders comprehensive project about and viva cheat sheet page."""
    return render_template("about.html")
