from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
from io import BytesIO

def get_sos_message():
    return (
        "🆘 I'm here for you. Let’s pause and breathe together... 🌬️\n\n"
        "**Scripture for Strength:** _'The Lord is my strength and my shield.'_ (Psalm 28:7)\n\n"
        "**You are not alone. You are loved. You are stronger than this.** 💪\n\n"
        "Would you like to talk about what you're feeling?"
    )

def get_reflection_prompt():
    return (
        "📝 Before we end today... take a moment to reflect:\n"
        "- What’s one thing you're grateful for?\n"
        "- What’s one challenge you faced?\n\n"
        "_Gratitude turns what we have into enough._ 🌅"
    )

def format_response_with_emojis(text: str) -> str:
    text = text.replace("God", "🙏 God")
    text = text.replace("peace", "🕊️ peace")
    text = text.replace("strength", "💪 strength")
    return text

def generate_ics(category, topic, total_days):
    cal = Calendar()
    cal.add("prodid", "-//DSCPL Spiritual Calendar//")
    cal.add("version", "2.0")

    start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    tz = pytz.timezone("Asia/Kolkata")

    for day in range(total_days):
        event = Event()
        event.add("summary", f"DSCPL Day {day+1} – {category}: {topic}")
        start_dt = tz.localize(start_date + timedelta(days=day))
        event.add("dtstart", start_dt)
        event.add("dtend", start_dt + timedelta(minutes=30))
        event.add("description", f"Spiritual {category.lower()} focus on '{topic}'")
        cal.add_component(event)

    buf = BytesIO()
    buf.write(cal.to_ical())
    return buf.getvalue()
