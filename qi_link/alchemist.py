"""
Alchemist - The Core L9 Logic
=============================

The metaphysical calculation engine that synthesizes destiny (fate)
and fortune (environment) to prescribe corrective energy remedies.

Now incorporates real-world Feng Shui factors:
- Ambient temperature (Fire/Water balance)
- Facing direction (8 compass directions with element associations)
- Weather conditions (humidity, wind)
"""

from typing import Optional, Dict, Any

from qi_link.config import get_settings
from qi_link.exceptions import AlchemyError, ElementImbalanceError
from qi_link.models import Diagnosis, Element, EnergyState, EnvironmentReading, FateProfile


class Alchemist:
    """
    The Brain of Qi-Link - Calculates metaphysical balance and
    generates corrective energy prescriptions.
    
    Feng Shui Algorithm incorporates:
    1. User's birth element (from Zi Wei Dou Shu)
    2. Machine environment (CPU temp, network latency)
    3. Real ambient temperature (weather)
    4. Facing direction (compass with Ba Gua associations)
    5. Weather conditions (humidity affects Water element)
    """

    # Direction to Element mapping (Ba Gua / 八卦)
    DIRECTION_ELEMENTS = {
        "north": Element.WATER,      # 坎 Kan
        "south": Element.FIRE,       # 離 Li
        "east": Element.WOOD,        # 震 Zhen
        "west": Element.METAL,       # 兌 Dui
        "northeast": Element.EARTH,  # 艮 Gen
        "southeast": Element.WOOD,   # 巽 Xun
        "southwest": Element.EARTH,  # 坤 Kun
        "northwest": Element.METAL,  # 乾 Qian
    }
    
    # Temperature thresholds for element mapping (Celsius)
    TEMP_FIRE_THRESHOLD = 30.0   # Hot = Fire energy
    TEMP_WATER_THRESHOLD = 10.0  # Cold = Water energy
    
    # Humidity thresholds
    HUMIDITY_HIGH_THRESHOLD = 70  # High humidity = Water influence
    HUMIDITY_LOW_THRESHOLD = 30   # Low humidity = Fire/Metal influence

    IMBALANCE_MATRIX = {
        (Element.METAL, Element.FIRE): {"en": "Metal melting in Fire - structure dissolving under pressure", "zh": "金逢火煉 - 過度壓力消融本質結構", "remedy": [Element.WATER, Element.EARTH]},
        (Element.METAL, Element.WATER): {"en": "Metal freezing in Water - clarity trapped in cold stillness", "zh": "金沉水底 - 清明之質困於寒滯", "remedy": [Element.FIRE, Element.EARTH]},
        (Element.METAL, Element.WOOD): {"en": "Metal cutting Wood - excessive control causing friction", "zh": "金木相剋 - 過度控制引發衝突", "remedy": [Element.WATER]},
        (Element.METAL, Element.EARTH): {"en": "Metal buried in Earth - potential hidden, waiting to shine", "zh": "金埋土中 - 潛能深藏，待時而發", "remedy": [Element.FIRE, Element.WATER]},
        (Element.WOOD, Element.METAL): {"en": "Wood cut by Metal - growth stunted by harsh constraints", "zh": "木受金傷 - 成長受阻於嚴苛約束", "remedy": [Element.WATER, Element.FIRE]},
        (Element.WOOD, Element.FIRE): {"en": "Wood feeding Fire - energy depleting through overgiving", "zh": "木火通明 - 過度付出耗損元氣", "remedy": [Element.WATER, Element.EARTH]},
        (Element.WOOD, Element.WATER): {"en": "Wood drowning in Water - excessive emotion stifling action", "zh": "水多木漂 - 情感泛濫阻礙行動", "remedy": [Element.FIRE, Element.EARTH]},
        (Element.WOOD, Element.EARTH): {"en": "Wood piercing Earth - conflict between growth and stability", "zh": "木剋土虛 - 成長與穩定之間的矛盾", "remedy": [Element.METAL, Element.FIRE]},
        (Element.WATER, Element.FIRE): {"en": "Water evaporating in Fire - wisdom lost to passion", "zh": "水火相激 - 智慧散於熱情之中", "remedy": [Element.METAL, Element.WOOD]},
        (Element.WATER, Element.EARTH): {"en": "Water dammed by Earth - flow blocked, stagnation forms", "zh": "土來剋水 - 流動受阻，停滯成形", "remedy": [Element.WOOD, Element.METAL]},
        (Element.WATER, Element.METAL): {"en": "Water chilled by Metal - too much clarity, frozen intuition", "zh": "金水太過 - 過度清明，直覺凍結", "remedy": [Element.FIRE, Element.WOOD]},
        (Element.WATER, Element.WOOD): {"en": "Water nurturing Wood - giving without receiving", "zh": "水生木旺 - 付出未得回報", "remedy": [Element.METAL, Element.EARTH]},
        (Element.FIRE, Element.WATER): {"en": "Fire extinguished by Water - passion quenched by cold logic", "zh": "水來滅火 - 熱情被冷靜邏輯澆熄", "remedy": [Element.WOOD, Element.EARTH]},
        (Element.FIRE, Element.METAL): {"en": "Fire melting Metal - destruction through transformation", "zh": "火煉金銷 - 蛻變中的毀滅", "remedy": [Element.EARTH, Element.WATER]},
        (Element.FIRE, Element.EARTH): {"en": "Fire exhausted into Earth - burnout from overproduction", "zh": "火生土晦 - 過度產出導致倦怠", "remedy": [Element.WOOD, Element.METAL]},
        (Element.FIRE, Element.WOOD): {"en": "Fire consuming Wood - growth sacrificed for illumination", "zh": "木火焚身 - 成長犧牲於光明", "remedy": [Element.WATER, Element.EARTH]},
        (Element.EARTH, Element.WOOD): {"en": "Earth penetrated by Wood - stability disrupted by change", "zh": "木剋土動 - 穩定被變化打破", "remedy": [Element.METAL, Element.FIRE]},
        (Element.EARTH, Element.WATER): {"en": "Earth eroded by Water - foundation slowly washing away", "zh": "水多土流 - 根基緩緩流失", "remedy": [Element.FIRE, Element.METAL]},
        (Element.EARTH, Element.FIRE): {"en": "Earth receiving Fire - absorption without action", "zh": "火生土滯 - 吸收而不作為", "remedy": [Element.METAL, Element.WOOD]},
        (Element.EARTH, Element.METAL): {"en": "Earth depleted by Metal - giving structure drains resources", "zh": "土生金洩 - 付出結構耗損資源", "remedy": [Element.FIRE, Element.WATER]},
    }

    BALANCED_REMEDY = {"en": "Elements in harmony - maintain current flow", "zh": "五行調和 - 維持當前能量流動", "remedy": []}

    def __init__(self):
        self._settings = get_settings()

    def diagnose(
        self, 
        fate: FateProfile, 
        environment: EnvironmentReading,
        real_environment: Optional[Dict[str, Any]] = None
    ) -> Diagnosis:
        """
        Perform comprehensive Feng Shui diagnosis.
        
        Args:
            fate: User's astrological profile from birth data
            environment: Machine sensor readings (CPU, network, etc.)
            real_environment: Real-world data dict with keys:
                - weather: WeatherData (temperature, humidity, etc.)
                - compass: CompassData (facing direction)
                - location: LocationData (city, country)
        
        Returns:
            Diagnosis with imbalance analysis and remedy prescription
        """
        user_element = fate.inherent_element
        
        # Calculate combined environmental element considering all factors
        env_element = self._calculate_combined_environment_element(
            environment, 
            real_environment
        )
        
        # Get additional modifiers from real environment
        env_modifiers = self._analyze_real_environment(real_environment)
        
        key = (user_element, env_element)
        imbalance_data = self.IMBALANCE_MATRIX.get(key)

        if imbalance_data is None:
            imbalance_data = self._find_weakness_remedy(fate, environment)
        
        # Adjust remedy based on environmental modifiers
        remedy_elements = self._adjust_remedy_for_environment(
            imbalance_data["remedy"].copy() if imbalance_data["remedy"] else [],
            env_modifiers,
            user_element
        )
        
        if not remedy_elements:
            remedy_elements = [self._get_generating_element(user_element)]

        # Build enhanced description with real-world factors
        description_en = self._build_enhanced_description(
            imbalance_data["en"],
            env_modifiers
        )

        talisman_prompt = self._generate_talisman_prompt(
            fate, environment, remedy_elements, description_en, real_environment
        )

        return Diagnosis(
            fate_profile=fate,
            environment=environment,
            imbalance_description=description_en,
            imbalance_description_chinese=imbalance_data["zh"],
            remedy_elements=remedy_elements,
            remedy_description=self._generate_remedy_description(remedy_elements, env_modifiers),
            talisman_prompt=talisman_prompt,
            talisman_style="Cyberpunk Taoist Talisman",
        )

    def _calculate_combined_environment_element(
        self,
        machine_env: EnvironmentReading,
        real_env: Optional[Dict[str, Any]]
    ) -> Element:
        """
        Calculate the dominant environmental element from all sources.
        
        Weighting:
        - Machine state (CPU/Network): 30%
        - Real ambient temperature: 35%
        - Facing direction: 35%
        
        Returns the element with highest combined score.
        """
        element_scores: Dict[Element, float] = {e: 0.0 for e in Element}
        
        # 1. Machine environment contribution (30%)
        machine_element = machine_env.dominant_environment_element
        element_scores[machine_element] += 0.30
        
        # 2. Real ambient temperature contribution (35%)
        if real_env and real_env.get("weather"):
            weather = real_env["weather"]
            temp = getattr(weather, 'temperature_celsius', 20.0)
            humidity = getattr(weather, 'humidity_percent', 50)
            
            # Temperature -> Element
            if temp >= self.TEMP_FIRE_THRESHOLD:
                element_scores[Element.FIRE] += 0.35
            elif temp <= self.TEMP_WATER_THRESHOLD:
                element_scores[Element.WATER] += 0.35
            elif temp > 20:
                # Warm but not hot - mild Fire + Earth
                element_scores[Element.FIRE] += 0.15
                element_scores[Element.EARTH] += 0.20
            else:
                # Cool but not cold - mild Water + Metal
                element_scores[Element.WATER] += 0.15
                element_scores[Element.METAL] += 0.20
            
            # Humidity modifier
            if humidity >= self.HUMIDITY_HIGH_THRESHOLD:
                element_scores[Element.WATER] += 0.10
            elif humidity <= self.HUMIDITY_LOW_THRESHOLD:
                element_scores[Element.FIRE] += 0.05
                element_scores[Element.METAL] += 0.05
        else:
            # No real weather data - distribute evenly
            element_scores[Element.EARTH] += 0.35
        
        # 3. Facing direction contribution (35%)
        if real_env and real_env.get("compass"):
            compass = real_env["compass"]
            direction = getattr(compass, 'cardinal_direction', '').lower()
            direction_element = self.DIRECTION_ELEMENTS.get(direction)
            
            if direction_element:
                element_scores[direction_element] += 0.35
            else:
                # Unknown direction - default to Earth (stability)
                element_scores[Element.EARTH] += 0.35
        else:
            # No compass data - distribute evenly
            element_scores[Element.EARTH] += 0.35
        
        # Return element with highest score
        return max(element_scores, key=element_scores.get)

    def _analyze_real_environment(
        self, 
        real_env: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze real environment for additional modifiers.
        
        Returns dict with:
        - temperature_influence: 'hot', 'cold', 'moderate'
        - humidity_influence: 'wet', 'dry', 'moderate'
        - direction_element: Element from facing direction
        - direction_name: Cardinal direction name
        - weather_condition: Current weather
        - location: City/region
        """
        modifiers = {
            "temperature_influence": "moderate",
            "humidity_influence": "moderate",
            "direction_element": None,
            "direction_name": None,
            "weather_condition": None,
            "location": None,
            "ambient_temp": None,
        }
        
        if not real_env:
            return modifiers
        
        # Weather analysis
        weather = real_env.get("weather")
        if weather:
            temp = getattr(weather, 'temperature_celsius', 20.0)
            humidity = getattr(weather, 'humidity_percent', 50)
            
            modifiers["ambient_temp"] = temp
            modifiers["weather_condition"] = getattr(weather, 'weather_condition', None)
            
            if temp >= self.TEMP_FIRE_THRESHOLD:
                modifiers["temperature_influence"] = "hot"
            elif temp <= self.TEMP_WATER_THRESHOLD:
                modifiers["temperature_influence"] = "cold"
            
            if humidity >= self.HUMIDITY_HIGH_THRESHOLD:
                modifiers["humidity_influence"] = "wet"
            elif humidity <= self.HUMIDITY_LOW_THRESHOLD:
                modifiers["humidity_influence"] = "dry"
        
        # Compass analysis
        compass = real_env.get("compass")
        if compass:
            direction = getattr(compass, 'cardinal_direction', '').lower()
            modifiers["direction_name"] = getattr(compass, 'cardinal_direction', None)
            modifiers["direction_element"] = self.DIRECTION_ELEMENTS.get(direction)
        
        # Location
        location = real_env.get("location")
        if location:
            city = getattr(location, 'city', None)
            country = getattr(location, 'country', None)
            if city and city != "Unknown":
                modifiers["location"] = f"{city}, {country}"
        
        return modifiers

    def _adjust_remedy_for_environment(
        self,
        base_remedy: list,
        env_modifiers: Dict[str, Any],
        user_element: Element
    ) -> list[Element]:
        """
        Adjust remedy elements based on real environmental factors.
        
        - Hot environment: Add Water to remedy (cooling)
        - Cold environment: Add Fire to remedy (warming)
        - High humidity: Reduce Water in remedy, add Earth (drainage)
        - Facing direction conflicts: Add generating element
        """
        remedy = list(base_remedy) if base_remedy else []
        
        # Temperature adjustments
        if env_modifiers["temperature_influence"] == "hot":
            if Element.WATER not in remedy and Element.FIRE in remedy:
                # Hot + Fire remedy = too much heat, add Water
                remedy.append(Element.WATER)
            elif Element.WATER not in remedy:
                # Hot environment, consider adding cooling Water
                if user_element != Element.FIRE:  # Unless user is Fire type
                    remedy.append(Element.WATER)
        
        elif env_modifiers["temperature_influence"] == "cold":
            if Element.FIRE not in remedy and Element.WATER in remedy:
                # Cold + Water remedy = too cold, add Fire
                remedy.append(Element.FIRE)
            elif Element.FIRE not in remedy:
                # Cold environment, consider adding warming Fire
                if user_element != Element.WATER:  # Unless user is Water type
                    remedy.append(Element.FIRE)
        
        # Humidity adjustments
        if env_modifiers["humidity_influence"] == "wet":
            # High humidity - Earth helps absorb excess Water
            if Element.EARTH not in remedy and len(remedy) < 3:
                remedy.append(Element.EARTH)
        
        # Direction element conflict resolution
        direction_element = env_modifiers.get("direction_element")
        if direction_element:
            # If facing a direction that conflicts with user element
            if direction_element.controls == user_element:
                # Add generating element to protect user
                protector = self._get_generating_element(user_element)
                if protector not in remedy and len(remedy) < 3:
                    remedy.append(protector)
        
        # Limit to max 3 remedy elements
        return remedy[:3] if remedy else [self._get_generating_element(user_element)]

    def _build_enhanced_description(
        self,
        base_description: str,
        env_modifiers: Dict[str, Any]
    ) -> str:
        """Build enhanced description including real-world factors."""
        parts = [base_description]
        
        # Add temperature influence
        if env_modifiers["temperature_influence"] == "hot":
            temp = env_modifiers.get("ambient_temp", 30)
            parts.append(f"Hot environment ({temp:.0f}C) intensifies Fire energy.")
        elif env_modifiers["temperature_influence"] == "cold":
            temp = env_modifiers.get("ambient_temp", 10)
            parts.append(f"Cold environment ({temp:.0f}C) amplifies Water energy.")
        
        # Add direction influence
        if env_modifiers["direction_name"] and env_modifiers["direction_element"]:
            direction = env_modifiers["direction_name"]
            element = env_modifiers["direction_element"]
            parts.append(f"Facing {direction} channels {element.value.title()} energy.")
        
        # Add weather condition
        if env_modifiers["weather_condition"]:
            condition = env_modifiers["weather_condition"]
            if "rain" in condition.lower():
                parts.append("Rain enhances Water element influence.")
            elif "clear" in condition.lower() or "sunny" in condition.lower():
                parts.append("Clear skies strengthen Fire/Metal clarity.")
            elif "cloud" in condition.lower():
                parts.append("Cloudy conditions moderate elemental extremes.")
        
        return " ".join(parts)

    def _find_weakness_remedy(self, fate: FateProfile, environment: EnvironmentReading) -> dict:
        weakest = fate.weakest_element
        return {
            "en": f"Element alignment detected - strengthening {weakest.value} to prevent deficiency",
            "zh": f"五行同氣 - 補強{weakest.chinese}以防不足",
            "remedy": [weakest, fate.inherent_element.generates],
        }

    def _get_generating_element(self, element: Element) -> Element:
        generation_cycle = {
            Element.METAL: Element.EARTH,
            Element.WATER: Element.METAL,
            Element.WOOD: Element.WATER,
            Element.FIRE: Element.WOOD,
            Element.EARTH: Element.FIRE,
        }
        return generation_cycle[element]

    def _generate_remedy_description(
        self, 
        elements: list[Element],
        env_modifiers: Optional[Dict[str, Any]] = None
    ) -> str:
        if not elements:
            return "Maintain current balance through mindful awareness."
        
        element_powers = {
            Element.METAL: "clarity and structure",
            Element.WOOD: "growth and flexibility",
            Element.WATER: "wisdom and adaptability",
            Element.FIRE: "passion and transformation",
            Element.EARTH: "stability and grounding",
        }
        powers = [element_powers[e] for e in elements]
        base = f"Channel {', '.join(powers)} to restore harmony."
        
        # Add direction-specific advice based on REMEDY ELEMENTS (what user needs)
        # Not based on current direction!
        primary_remedy = elements[0] if elements else None
        
        if primary_remedy:
            # Direction advice should help user GET the remedy element
            remedy_direction_advice = {
                Element.FIRE: "Face South to harness Fire energy, or add Wood (green plants, growth activities) as a bridge - Water generates Wood, Wood generates Fire.",
                Element.WATER: "Face North to channel Water wisdom, or embrace Metal (white, clarity, structure) which generates Water.",
                Element.WOOD: "Face East to absorb Wood's growth energy, or connect with Water (meditation, flow) which nourishes Wood.",
                Element.METAL: "Face West to receive Metal's clarity, or cultivate Earth (stability, grounding) which generates Metal.",
                Element.EARTH: "Face Southwest or Northeast for Earth grounding, or kindle Fire (passion, action) which creates Earth.",
            }
            
            if primary_remedy in remedy_direction_advice:
                base += f" {remedy_direction_advice[primary_remedy]}"
        
        # Add Wu Xing generation cycle explanation if multiple remedy elements
        if len(elements) >= 2:
            cycle_explanations = []
            for i in range(len(elements) - 1):
                e1, e2 = elements[i], elements[i + 1]
                if e1.generates == e2:
                    cycle_explanations.append(f"{e1.chinese}({e1.value.title()}) generates {e2.chinese}({e2.value.title()})")
            
            if cycle_explanations:
                base += f" Flow: {' → '.join(cycle_explanations)}."
        
        return base

    def _generate_talisman_prompt(
        self, 
        fate: FateProfile, 
        environment: EnvironmentReading, 
        remedy_elements: list[Element], 
        imbalance_en: str,
        real_environment: Optional[Dict[str, Any]] = None
    ) -> str:
        star_name = fate.major_star.value
        element_visuals = {
            Element.METAL: ("silver and white", "geometric patterns, crystals, circuits"),
            Element.WOOD: ("emerald green and cyan", "bamboo, vines, digital roots"),
            Element.FIRE: ("crimson and orange", "flames, phoenixes, plasma arcs"),
            Element.WATER: ("deep blue and aqua", "waves, dragons, data streams"),
            Element.EARTH: ("golden amber and brown", "mountains, hexagons, solid foundations"),
        }

        colors, symbols = [], []
        for elem in remedy_elements:
            c, s = element_visuals[elem]
            colors.append(c)
            symbols.append(s)

        color_palette = ", ".join(colors) if colors else "mystical purple and gold"
        symbol_elements = ", ".join(symbols) if symbols else "ancient sigils"

        # Environment energy description
        if environment.temperature_state == EnergyState.EXCESS:
            env_energy = "crackling with excess yang energy"
        elif environment.temperature_state == EnergyState.DEFICIENT:
            env_energy = "glowing with deep yin stillness"
        else:
            env_energy = "pulsing with balanced chi"
        
        # Add real-world weather influence to prompt
        weather_influence = ""
        direction_influence = ""
        
        if real_environment:
            weather = real_environment.get("weather")
            compass = real_environment.get("compass")
            
            if weather:
                condition = getattr(weather, 'weather_condition', '')
                if "rain" in condition.lower():
                    weather_influence = ", with mystical rain drops falling through the digital void"
                elif "cloud" in condition.lower():
                    weather_influence = ", with ethereal clouds of data mist"
                elif "clear" in condition.lower():
                    weather_influence = ", under a clear digital sky with stars"
            
            if compass:
                direction = getattr(compass, 'cardinal_direction', '')
                if direction:
                    direction_influence = f", oriented towards the {direction} with corresponding Ba Gua trigram symbols"

        return f"""A mystical cyberpunk Taoist talisman, hyper-detailed digital art, 8K resolution.
Central motif: The {star_name} constellation rendered as a glowing neon sigil, surrounded by {symbol_elements}.
Color scheme: Dominant {color_palette}, with accents of electric purple and holographic gold.
Background: Dark void filled with subtle circuit patterns and ancient Chinese calligraphy floating like data code, {env_energy}{weather_influence}{direction_influence}.
Style: Fusion of traditional Chinese fu-lu (符籙) talisman art with cyberpunk aesthetics.
Text elements: Integrate the characters "{remedy_elements[0].chinese if remedy_elements else '氣'}" in a stylized, glowing font.
Quality: Masterpiece, trending on ArtStation, concept art, highly detailed, sharp focus, dramatic lighting."""

    def get_element_relationship(self, element1: Element, element2: Element) -> str:
        if element1.generates == element2:
            return f"{element1.chinese} generates {element2.chinese}"
        elif element1.controls == element2:
            return f"{element1.chinese} controls {element2.chinese}"
        elif element2.generates == element1:
            return f"{element2.chinese} generates {element1.chinese}"
        elif element2.controls == element1:
            return f"{element2.chinese} controls {element1.chinese}"
        else:
            return f"{element1.chinese} and {element2.chinese} are in indirect relationship"
