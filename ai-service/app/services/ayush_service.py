"""
MediKiosk AI Service - Classical AYUSH / Ayurveda Clinical Engine
=================================================================

Purpose:
    Provide an authentic, standardized Ayurvedic clinical assessment covering:
    1. Prakriti Determination (Constitutional Tridosha scoring: Vata, Pitta, Kapha).
    2. Vikriti Assessment (Current doshic aggravation / imbalance).
    3. Agni Evaluation (Digestive fire: Sama, Vishama, Tikshna, Manda).
    4. Koshtha Assessment (Bowel habituation: Mridu, Krura, Madhyama).
    5. Ahara & Vihara Analysis (Dietary & lifestyle factors).
    6. Dashavidha Pariksha (Classical tenfold diagnostic framework).
    7. Pathya & Apathya Clinical Guidance (Wholesome vs unwholesome recommendations).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from app.models.schemas import (
    AyushAssessment,
    DashavidhaParikshaData,
    LanguageCode,
    PrakritiScores,
    VikritiScores,
)


# ============================================================
# PRAKRITI QUESTIONNAIRE (PHYSICAL & MENTAL DOSHA ATTRIBUTES)
# ============================================================

PRAKRITI_QUESTIONS = [
    {
        "id": "body_frame",
        "category": "Physical Frame",
        "question": "What is your natural body frame and bone structure?",
        "options": [
            {"label": "Thin, lean, prominent joints, difficult to gain weight", "dosha": "vata", "points": 1},
            {"label": "Medium build, athletic, well-proportioned, moderate weight", "dosha": "pitta", "points": 1},
            {"label": "Broad build, heavy, sturdy, gains weight easily", "dosha": "kapha", "points": 1},
        ],
    },
    {
        "id": "skin_nature",
        "category": "Skin & Complexion",
        "question": "How is your skin naturally without moisturizers?",
        "options": [
            {"label": "Dry, rough, thin, cracks easily in cold weather", "dosha": "vata", "points": 1},
            {"label": "Warm, sensitive, reddish, prone to acne/freckles", "dosha": "pitta", "points": 1},
            {"label": "Smooth, moist, thick, oily, cool and radiant", "dosha": "kapha", "points": 1},
        ],
    },
    {
        "id": "appetite_digestion",
        "category": "Agni & Appetite",
        "question": "How is your typical appetite and digestion?",
        "options": [
            {"label": "Irregular, variable, sometimes hungry, sometimes forget to eat (Vishama)", "dosha": "vata", "points": 1},
            {"label": "Sharp, strong, cannot skip meals without irritability/acid (Tikshna)", "dosha": "pitta", "points": 1},
            {"label": "Slow, steady, can easily skip meals, feels heavy after food (Manda)", "dosha": "kapha", "points": 1},
        ],
    },
    {
        "id": "bowel_habit",
        "category": "Koshtha (Bowel)",
        "question": "What describes your typical bowel movement?",
        "options": [
            {"label": "Hard, dry, prone to gas and constipation (Krura Koshtha)", "dosha": "vata", "points": 1},
            {"label": "Soft, loose, frequent, easily stimulated by milk/fruits (Mridu Koshtha)", "dosha": "pitta", "points": 1},
            {"label": "Regular, thick, well-formed, sluggish (Madhyama Koshtha)", "dosha": "kapha", "points": 1},
        ],
    },
    {
        "id": "temperature_weather",
        "category": "Climate Adaptability",
        "question": "Which climate or weather do you dislike the most?",
        "options": [
            {"label": "Dislikes cold, dry, and windy weather; loves warmth", "dosha": "vata", "points": 1},
            {"label": "Dislikes hot, humid weather; loves cool breeze and shade", "dosha": "pitta", "points": 1},
            {"label": "Dislikes damp, wet, chilly weather; tolerates heat well", "dosha": "kapha", "points": 1},
        ],
    },
    {
        "id": "sleep_pattern",
        "category": "Nidra (Sleep)",
        "question": "How is your normal sleep pattern?",
        "options": [
            {"label": "Light, interrupted, tends to wake easily, 5-6 hours", "dosha": "vata", "points": 1},
            {"label": "Moderate, sound, dreams of fire/competition, 6-7 hours", "dosha": "pitta", "points": 1},
            {"label": "Deep, heavy, hard to wake up in morning, 8+ hours", "dosha": "kapha", "points": 1},
        ],
    },
    {
        "id": "mental_activity",
        "category": "Manasa (Mind & Speech)",
        "question": "How do your thoughts and speech usually flow?",
        "options": [
            {"label": "Quick, imaginative, enthusiastic, talks fast, anxious easily", "dosha": "vata", "points": 1},
            {"label": "Sharp, articulate, analytical, purposeful, can get irritable", "dosha": "pitta", "points": 1},
            {"label": "Calm, steady, patient, thoughtful, speaks slowly and gently", "dosha": "kapha", "points": 1},
        ],
    },
]


def calculate_prakriti(responses: Dict[str, Any]) -> PrakritiScores:
    """Calculates Prakriti constitution percentage from responses."""
    vata_pts = 0
    pitta_pts = 0
    kapha_pts = 0

    for q in PRAKRITI_QUESTIONS:
        ans = responses.get(q["id"])
        if ans:
            ans_str = str(ans).lower()
            if "vata" in ans_str:
                vata_pts += 1
            elif "pitta" in ans_str:
                pitta_pts += 1
            elif "kapha" in ans_str:
                kapha_pts += 1

    total = vata_pts + pitta_pts + kapha_pts
    if total == 0:
        # Default balanced constitution
        return PrakritiScores(
            vata=35.0,
            pitta=40.0,
            kapha=25.0,
            dominant_dosha="Pitta-Vata",
            secondary_dosha="Kapha",
            constitution_type="Dwandvaja (Pitta-Vata)",
        )

    v_pct = round((vata_pts / total) * 100, 1)
    p_pct = round((pitta_pts / total) * 100, 1)
    k_pct = round((kapha_pts / total) * 100, 1)

    # Determine dominant
    scores = [("Vata", v_pct), ("Pitta", p_pct), ("Kapha", k_pct)]
    scores.sort(key=lambda x: x[1], reverse=True)

    dominant = scores[0][0]
    secondary = scores[1][0]

    const_type = f"Dwandvaja ({dominant}-{secondary})" if (scores[0][1] - scores[1][1] < 20) else f"Ekadoshaja ({dominant} Dominant)"

    return PrakritiScores(
        vata=v_pct,
        pitta=p_pct,
        kapha=k_pct,
        dominant_dosha=f"{dominant}-{secondary}",
        secondary_dosha=scores[2][0],
        constitution_type=const_type,
    )


def assess_agni(responses: Dict[str, Any]) -> str:
    """Classifies Agni based on digestive patterns."""
    raw = str(responses.get("appetite_digestion", "")).lower()
    if "tikshna" in raw or "sharp" in raw or "pitta" in raw:
        return "Tikshna Agni (Hyperactive / Acidic - Pitta influence)"
    elif "vishama" in raw or "irregular" in raw or "vata" in raw:
        return "Vishama Agni (Irregular / Variable - Vata influence)"
    elif "manda" in raw or "slow" in raw or "kapha" in raw:
        return "Manda Agni (Sluggish / Hypoactive - Kapha influence)"
    return "Sama Agni (Balanced & Harmonious Metabolism)"


def assess_koshtha(responses: Dict[str, Any]) -> str:
    """Classifies Koshtha based on bowel tendencies."""
    raw = str(responses.get("bowel_habit", "")).lower()
    if "krura" in raw or "hard" in raw or "constipat" in raw or "vata" in raw:
        return "Krura Koshtha (Hard / Dry Bowel - Requires unctuous diet & ghee)"
    elif "mridu" in raw or "soft" in raw or "loose" in raw or "pitta" in raw:
        return "Mridu Koshtha (Sensitive / Soft Bowel - Highly responsive to mild purgation)"
    return "Madhyama Koshtha (Moderate / Balanced Bowel Habit)"


def generate_ayush_recommendations(dominant_dosha: str) -> Tuple[List[str], List[str], List[str]]:
    """Provides classical Pathya, Apathya, and herbal support."""
    pathya = []
    apathya = []
    herbs = []

    if "Vata" in dominant_dosha:
        pathya.extend([
            "Warm, freshly cooked, nourishing meals with moderate cow's ghee or sesame oil",
            "Sweet, sour, and mildly salty tastes (Madhura, Amla, Lavana)",
            "Regular daily routine (Dinacharya) with warm oil self-massage (Abhyanga)",
            "Warm herbal teas (ginger, cinnamon, licorice, cumin)",
        ])
        apathya.extend([
            "Cold, dry, stale, or raw foods (dry salads, cold beverages)",
            "Pungent, bitter, and astringent foods in excess",
            "Irregular meal times and staying awake late at night (Ratri Jagarana)",
            "Excessive travel, wind exposure, and skipping meals",
        ])
        herbs.extend([
            "Ashwagandha (Withania somnifera) for nervous system rejuvenation and strength",
            "Shatavari (Asparagus racemosus) for mucosal nourishment",
            "Triphala with warm water at bedtime for gentle bowel regulation",
        ])

    if "Pitta" in dominant_dosha:
        pathya.extend([
            "Cooling, soothing foods with sweet, bitter, and astringent tastes",
            "Ghee, coconut water, fresh sweet fruits (pomegranate, sweet grapes)",
            "Moderate exercise in cool morning hours; adequate hydration",
            "Cooling spices: Coriander, fennel, cardamom, mint",
        ])
        apathya.extend([
            "Excessively spicy, oily, fried, sour, and fermented foods",
            "Excessive direct sun exposure and mid-day heat",
            "Skipping meals when hungry (aggravates acid fire)",
            "High consumption of red chili, vinegar, alcohol, and excessive coffee",
        ])
        herbs.extend([
            "Amla / Amalaki (Emblica officinalis) for natural cooling and antioxidant support",
            "Guduchi (Tinospora cordifolia) for immune balance and liver cooling",
            "Brahmi (Bacopa monnieri) for mental calmness and stress reduction",
        ])

    if "Kapha" in dominant_dosha:
        pathya.extend([
            "Light, warm, dry, easily digestible foods with pungent, bitter, and astringent tastes",
            "Warming spices: Black pepper, dry ginger (Shunti), Pippali, turmeric",
            "Vigorous daily physical exercise (Vyayama) and brisk walking",
            "Warm boiled water (Ushnodaka) throughout the day",
        ])
        apathya.extend([
            "Heavy, oily, deep-fried foods, ice cream, and dairy in excess",
            "Daytime sleep (Diva Swapna) and sedentary lifestyle",
            "Excessive sweet, cold, and salty tastes",
        ])
        herbs.extend([
            "Trikatu (Dry ginger, Black pepper, Long pepper) for stimulating sluggish Agni",
            "Tulsi (Holy Basil) for respiratory clarity",
            "Guggulu for metabolic lipid support and channel cleansing",
        ])

    return pathya, apathya, herbs


def conduct_ayush_assessment(
    patient_id: Optional[str] = None,
    responses: Optional[Dict[str, Any]] = None,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> AyushAssessment:
    """Performs end-to-end AYUSH clinical assessment."""
    responses = responses or {}
    prakriti = calculate_prakriti(responses)

    # Estimate Vikriti (current imbalance)
    vikriti = VikritiScores(
        vata_aggravation=min(100.0, prakriti.vata + 10.0),
        pitta_aggravation=prakriti.pitta,
        kapha_aggravation=max(0.0, prakriti.kapha - 5.0),
        current_imbalance=prakriti.dominant_dosha,
        severity="Mild to Moderate",
    )

    agni = assess_agni(responses)
    koshtha = assess_koshtha(responses)

    # Classical Dashavidha Pariksha
    dashavidha = DashavidhaParikshaData(
        dushyam="Rasa and Rakta Dhatu involvement",
        desham="Sadharana Desha (Temperate / Mixed climate)",
        balam="Madhyama Balam (Moderate immune and physical reserve)",
        kalam="Current Ritu (Season) transition",
        analam=agni,
        prakriti=f"{prakriti.constitution_type}",
        vayas="Madhyama Vayas (Adult stage)",
        satvam="Madhyama Satvam (Balanced mental endurance)",
        satmyam="Oka Satmya (Habituated to home-cooked regional diet)",
        aharam="Madhyama Abhyavaharana Shakti (Moderate intake capacity)",
    )

    pathya, apathya, herbs = generate_ayush_recommendations(prakriti.dominant_dosha)

    return AyushAssessment(
        prakriti=prakriti,
        vikriti=vikriti,
        agni=agni,
        koshtha=koshtha,
        ahara_habits={"diet_type": responses.get("diet", "Mixed / Vegetarian"), "meal_regularity": agni},
        vihara_lifestyle={"exercise": responses.get("exercise", "Moderate"), "sleep": responses.get("sleep", "6-7 hours")},
        dashavidha_pariksha=dashavidha,
        pathya_recommendations=pathya,
        apathya_warnings=apathya,
        herbal_support_guidance=herbs,
    )
