"""
Talisman Generator - AI Image Generation
=========================================

Handles talisman image generation using OpenAI DALL-E 3
with mock fallback for development.
"""

import base64
from qi_link.config import get_settings
from qi_link.exceptions import APIKeyMissingError, ImageGenerationError
from qi_link.models import Diagnosis, Element


class TalismanGenerator:
    """AI-powered talisman image generator using DALL-E 3."""

    # Ba Gua trigrams for each element
    BAGUA_SYMBOLS = {
        Element.METAL: ("☰", "乾"),
        Element.WOOD: ("☴", "巽"),
        Element.WATER: ("☵", "坎"),
        Element.FIRE: ("☲", "離"),
        Element.EARTH: ("☷", "坤"),
    }

    def __init__(self):
        self._settings = get_settings()
        self._openai_client = None

    def _get_openai_client(self):
        if self._openai_client is None:
            if not self._settings.has_openai_key:
                raise APIKeyMissingError()
            from openai import OpenAI
            self._openai_client = OpenAI(api_key=self._settings.openai_api_key.get_secret_value())
        return self._openai_client

    def generate(self, diagnosis: Diagnosis) -> str:
        if self._settings.mock_mode or not self._settings.has_openai_key:
            return self._generate_mock_talisman(diagnosis)
        return self._generate_dalle_talisman(diagnosis)

    def _generate_dalle_talisman(self, diagnosis: Diagnosis) -> str:
        try:
            client = self._get_openai_client()
            response = client.images.generate(
                model=self._settings.openai_model,
                prompt=diagnosis.talisman_prompt,
                size=self._settings.openai_image_size,
                quality=self._settings.openai_image_quality,
                n=1,
            )
            return response.data[0].url
        except APIKeyMissingError:
            raise
        except Exception as e:
            raise ImageGenerationError(
                message=f"DALL-E generation failed: {str(e)}", 
                details={"model": self._settings.openai_model}
            )

    def _generate_mock_talisman(self, diagnosis: Diagnosis) -> str:
        """Generate a circular mandala talisman SVG."""
        primary_element = diagnosis.primary_remedy_element
        secondary_element = (
            diagnosis.remedy_elements[1] 
            if len(diagnosis.remedy_elements) > 1 
            else diagnosis.fate_profile.inherent_element
        )
        
        colors = self._get_element_colors(primary_element)
        secondary_colors = self._get_element_colors(secondary_element)
        
        star_symbol = diagnosis.fate_profile.major_star.value
        element_char = primary_element.chinese
        bagua_symbol, _ = self.BAGUA_SYMBOLS.get(primary_element, ("☯", "道"))
        
        # Four pillars
        pillars = diagnosis.fate_profile
        
        svg = self._create_circular_talisman(
            colors=colors,
            secondary_colors=secondary_colors,
            star_symbol=star_symbol,
            element_char=element_char,
            bagua_symbol=bagua_symbol,
            pillars=pillars,
            remedy_elements=diagnosis.remedy_elements
        )
        
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64}"

    def _get_element_colors(self, element: Element) -> dict:
        palettes = {
            Element.METAL: {
                "primary": "#C0C0C0",
                "secondary": "#E8E8E8", 
                "accent": "#FFFFFF",
                "glow": "#FFFFFF",
                "dark": "#808080"
            },
            Element.WOOD: {
                "primary": "#00CC66",
                "secondary": "#00FF88",
                "accent": "#66FFAA",
                "glow": "#00FF88",
                "dark": "#008844"
            },
            Element.WATER: {
                "primary": "#0088FF",
                "secondary": "#00BFFF",
                "accent": "#66D9FF",
                "glow": "#00BFFF",
                "dark": "#0055AA"
            },
            Element.FIRE: {
                "primary": "#FF4400",
                "secondary": "#FF6600",
                "accent": "#FFAA00",
                "glow": "#FF6600",
                "dark": "#CC2200"
            },
            Element.EARTH: {
                "primary": "#DDAA00",
                "secondary": "#FFD700",
                "accent": "#FFEE66",
                "glow": "#FFD700",
                "dark": "#AA7700"
            },
        }
        return palettes.get(element, palettes[Element.FIRE])

    def _create_circular_talisman(
        self, colors, secondary_colors, star_symbol, element_char,
        bagua_symbol, pillars, remedy_elements
    ) -> str:
        """Create a circular mandala talisman with strong visual effects."""
        
        p = colors["primary"]
        s = colors["secondary"]
        a = colors["accent"]
        g = colors["glow"]
        d = colors["dark"]
        sp = secondary_colors["primary"]
        
        year = pillars.year_stem_branch
        month = pillars.month_stem_branch
        day = pillars.day_stem_branch
        hour = pillars.hour_stem_branch
        
        remedy_chars = " ".join([e.chinese for e in remedy_elements])
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
<defs>
    <!-- Radial gradient background -->
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="60%">
        <stop offset="0%" stop-color="#0a0a12"/>
        <stop offset="70%" stop-color="#050508"/>
        <stop offset="100%" stop-color="#000002"/>
    </radialGradient>
    
    <!-- Element color gradients -->
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{g}" stop-opacity="0.4"/>
        <stop offset="50%" stop-color="{p}" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="{d}" stop-opacity="0"/>
    </radialGradient>
    
    <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{s}"/>
        <stop offset="50%" stop-color="{p}"/>
        <stop offset="100%" stop-color="{d}"/>
    </linearGradient>
    
    <!-- Strong glow filter -->
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    
    <filter id="strongGlow" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur stdDeviation="8" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="blur"/>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
    
    <filter id="outerGlow" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur stdDeviation="15" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="blur"/>
        </feMerge>
    </filter>
</defs>

<style>
    /* Slow rotation animation */
    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    @keyframes rotateReverse {{
        from {{ transform: rotate(360deg); }}
        to {{ transform: rotate(0deg); }}
    }}
    
    /* Pulsing glow animation */
    @keyframes pulse {{
        0%, 100% {{ opacity: 0.4; }}
        50% {{ opacity: 0.8; }}
    }}
    
    @keyframes pulseSlow {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
    }}
    
    /* Breathing scale animation */
    @keyframes breathe {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
    }}
    
    /* Floating animation */
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    .rotate-slow {{ 
        animation: rotate 60s linear infinite; 
        transform-origin: 300px 300px;
    }}
    
    .rotate-medium {{ 
        animation: rotate 30s linear infinite; 
        transform-origin: 300px 300px;
    }}
    
    .rotate-reverse {{ 
        animation: rotateReverse 45s linear infinite; 
        transform-origin: 300px 300px;
    }}
    
    .pulse {{ animation: pulse 3s ease-in-out infinite; }}
    .pulse-slow {{ animation: pulseSlow 5s ease-in-out infinite; }}
    .breathe {{ animation: breathe 4s ease-in-out infinite; transform-origin: 300px 300px; }}
    .float {{ animation: float 3s ease-in-out infinite; }}
</style>

<!-- Background -->
<rect width="600" height="600" fill="url(#bgGrad)"/>

<!-- Center glow effect - breathing -->
<circle cx="300" cy="300" r="250" fill="url(#glowGrad)" class="pulse-slow"/>

<!-- Outer energy ring - glowing and pulsing -->
<circle cx="300" cy="300" r="270" fill="none" stroke="{g}" stroke-width="2" opacity="0.3" filter="url(#outerGlow)" class="pulse"/>
<circle cx="300" cy="300" r="260" fill="none" stroke="{p}" stroke-width="4" filter="url(#strongGlow)" class="breathe"/>

<!-- Decorative outer ring - slow rotation -->
<circle cx="300" cy="300" r="245" fill="none" stroke="{s}" stroke-width="1.5" stroke-dasharray="8,4,2,4" opacity="0.8" filter="url(#glow)" class="rotate-slow"/>

<!-- Main ring -->
<circle cx="300" cy="300" r="220" fill="none" stroke="url(#ringGrad)" stroke-width="3" filter="url(#glow)"/>

<!-- Inner decorative ring - reverse rotation -->
<circle cx="300" cy="300" r="195" fill="none" stroke="{p}" stroke-width="1" stroke-dasharray="20,10" opacity="0.6" class="rotate-reverse"/>

<!-- Rotating energy lines - medium speed rotation -->
<g filter="url(#glow)" class="rotate-medium">
    {"".join([f'<line x1="300" y1="{300-180}" x2="300" y2="{300-220}" stroke="{a}" stroke-width="2" opacity="0.7" transform="rotate({i*30}, 300, 300)"/>' for i in range(12)])}
</g>

<!-- Energy dots on outer ring - pulsing -->
<g filter="url(#strongGlow)" class="pulse">
    <circle cx="300" cy="65" r="5" fill="{s}"/>
    <circle cx="418" cy="118" r="5" fill="{s}"/>
    <circle cx="482" cy="235" r="5" fill="{s}"/>
    <circle cx="482" cy="365" r="5" fill="{s}"/>
    <circle cx="418" cy="482" r="5" fill="{s}"/>
    <circle cx="300" cy="535" r="5" fill="{s}"/>
    <circle cx="182" cy="482" r="5" fill="{s}"/>
    <circle cx="118" cy="365" r="5" fill="{s}"/>
    <circle cx="118" cy="235" r="5" fill="{s}"/>
    <circle cx="182" cy="118" r="5" fill="{s}"/>
</g>

<!-- Octagon frame - breathing -->
<polygon points="300,135 417,183 465,300 417,417 300,465 183,417 135,300 183,183" 
         fill="none" stroke="{a}" stroke-width="2" opacity="0.8" filter="url(#glow)" class="breathe"/>

<!-- Inner octagon - slow rotation -->
<polygon points="300,180 380,220 420,300 380,380 300,420 220,380 180,300 220,220" 
         fill="none" stroke="{p}" stroke-width="1" opacity="0.5" class="rotate-slow"/>

<!-- Ba Gua trigrams around the circle -->
<g font-family="serif" font-size="22" fill="{s}" filter="url(#glow)">
    <text x="300" y="100" text-anchor="middle">☰</text>
    <text x="442" y="158" text-anchor="middle">☱</text>
    <text x="500" y="305" text-anchor="middle">☲</text>
    <text x="442" y="450" text-anchor="middle">☳</text>
    <text x="300" y="510" text-anchor="middle">☴</text>
    <text x="158" y="450" text-anchor="middle">☵</text>
    <text x="100" y="305" text-anchor="middle">☶</text>
    <text x="158" y="158" text-anchor="middle">☷</text>
</g>

<!-- Central star symbol - main focus with floating animation -->
<text x="300" y="280" font-family="serif" font-size="72" fill="{s}" text-anchor="middle" filter="url(#strongGlow)" class="float">{star_symbol}</text>

<!-- Element character - pulsing -->
<text x="300" y="350" font-family="serif" font-size="48" fill="{a}" text-anchor="middle" filter="url(#strongGlow)" class="pulse">{element_char}</text>

<!-- Ba Gua symbol -->
<text x="300" y="400" font-family="serif" font-size="32" fill="{p}" text-anchor="middle" opacity="0.9" filter="url(#glow)" class="pulse-slow">{bagua_symbol}</text>

<!-- Four Pillars at cardinal positions -->
<g font-family="serif" font-size="16" fill="{s}" filter="url(#glow)">
    <text x="300" y="145" text-anchor="middle">{year}</text>
    <text x="455" y="305" text-anchor="middle">{month}</text>
    <text x="300" y="475" text-anchor="middle">{day}</text>
    <text x="145" y="305" text-anchor="middle">{hour}</text>
</g>

<!-- Remedy elements at bottom -->
<text x="300" y="545" font-family="serif" font-size="14" fill="{p}" text-anchor="middle" opacity="0.7">REMEDY</text>
<text x="300" y="575" font-family="serif" font-size="28" fill="{a}" text-anchor="middle" filter="url(#strongGlow)">{remedy_chars}</text>

<!-- Subtle pulsing inner circle -->
<circle cx="300" cy="300" r="130" fill="none" stroke="{g}" stroke-width="1" opacity="0.4" filter="url(#glow)"/>
<circle cx="300" cy="300" r="100" fill="none" stroke="{p}" stroke-width="0.5" opacity="0.3"/>

</svg>'''
