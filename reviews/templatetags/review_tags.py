from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def star_rating(rating):
    """
    Generates a string of SVG icons for star ratings, correctly handling full, half, and empty stars.
    """
    if rating is None:
        rating = 0
    
    try:
        # Ensure rating is a valid number
        rating = float(rating)
    except (ValueError, TypeError):
        rating = 0

    # --- SVG Icons ---
    # These icons are designed to be styled by CSS on the page (e.g., color, size).
    
    # A full, solid star
    svg_star_full = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>'
    
    # A half-filled star icon
    svg_star_half = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292zM10 1.26v13.51l5.878 4.26-2.22-6.883 5.342-4.632-6.98-.602L10 1.26z" clip-rule="evenodd" /></svg>'

    # An empty star (outline)
    svg_star_empty = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.31h5.418a.562.562 0 01.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-3.356a.563.563 0 00-.652 0l-4.725 3.356a.562.562 0 01-.84-.61l1.285-5.385a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988h5.418a.563.563 0 00.475-.31L11.48 3.5z" /></svg>'

    # --- New, Clearer Logic ---
    # Get the whole number of stars
    full_stars_count = int(rating)
    
    # Get the decimal part to determine rounding or half-star
    decimal = rating - full_stars_count

    # Determine how many of each star type to show
    if decimal >= 0.75:
        full_stars_count += 1
        half_star_count = 0
    elif decimal >= 0.25:
        half_star_count = 1
    else:
        half_star_count = 0

    empty_stars_count = 5 - full_stars_count - half_star_count

    # Build the final HTML string
    stars_html = (
        (svg_star_full * full_stars_count) +
        (svg_star_half * half_star_count) +
        (svg_star_empty * empty_stars_count)
    )

    return mark_safe(stars_html)