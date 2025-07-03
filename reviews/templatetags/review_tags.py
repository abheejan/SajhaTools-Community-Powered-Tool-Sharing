from django import template
from django.utils.safestring import mark_safe # <--- IMPORT THIS

register = template.Library()

@register.simple_tag
def star_rating(rating):
    if rating is None or rating == 0:
        return "" 
        
    full_stars = int(rating)

    half_star = 1 if (rating - full_stars) >= 0.25 and (rating - full_stars) < 0.75 else 0
    
    full_stars = round(rating - (0.5 if half_star else 0)) 
    empty_stars = 5 - full_stars - half_star
    

    svg_star_full = '<svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>'
    
    svg_star_empty = '<svg class="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 2.929l1.455 4.47-4.298.001 3.284 2.39-1.245 4.093 3.523-2.617 3.524 2.617-1.246-4.093 3.284-2.39-4.298-.001L10 2.929zM10 1c.58 0 1.05.513  .874 1.248l-1.45 4.469 4.298.001c.792 0 1.137 1.01.53 1.543l-3.283 2.39 1.245 4.092c.28.92-.81 1.64-1.61.99l-3.524-2.618-3.523 2.618c-.8.65-1.89-.07-1.61-.99l1.246-4.092-3.284-2.39c-.607-.533-.262-1.543.53-1.543l4.298-.001-1.45-4.469C8.95.513 9.42 1 10 1z" clip-rule="evenodd"></path></svg>'
    
   
    
    stars_html = (
        svg_star_full * full_stars +
        svg_star_empty * (5 - full_stars) 
    )


    return mark_safe(stars_html)