import json
import requests
import streamlit as st
from PIL import Image

API_BASE = "https://pfa-faq-generator-production.up.railway.app/"   # change if your API runs elsewhere
ENDPOINT = f"{API_BASE}/generate-faq"

icon = Image.open("assets/icon.png")
st.set_page_config(page_title="FAQ Generator", page_icon=icon)
st.title("FAQ Generator")
st.write("Paste a URL, generate a structured FAQ, and download JSON.")

url = st.text_input("Website URL", placeholder="https://example.com")


col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("Generate FAQ")


if generate:
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        with st.spinner("Fetching, cleaning, and extracting FAQ..."):
            try:
                payload = {"url": url.strip()}
                r = requests.post(ENDPOINT, json=payload, timeout=120)
                r.raise_for_status()
                data = r.json()
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
                st.stop()
            except ValueError:
                st.error("API returned non-JSON response.")
                st.stop()

        st.success("Done!")

        # Show metadata if present
        if "site_url" in data:
            st.caption(f"site_url: {data.get('site_url')}")
        if "page_url" in data:
            st.caption(f"page_url: {data.get('page_url')}")

        items = data.get("items", [])
        if not items:
            st.info("No FAQ items were extracted (page might not contain clear Q/A content).")
        else:
            # Group by theme
            grouped = {}
            for it in items:
                grouped.setdefault(it.get("theme", "Other"), []).append(it)

            for theme, theme_items in grouped.items():
                with st.expander(f"{theme} ({len(theme_items)})", expanded=False):
                    for it in theme_items:
                        st.markdown(f"**Q:** {it.get('question','')}")
                        st.markdown(f"**A:** {it.get('answer','')}")
                        conf = it.get("confidence", None)
                        if conf is not None:
                            st.caption(f"confidence: {conf}")
                        src = it.get("sources", [])
                        if src:
                            st.caption("sources: " + ", ".join(src))
                        st.divider()

        # Download button
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            "Download JSON",
            data=json_str,
            file_name="faq.json",
            mime="application/json",
        )
        
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 0.9em; color: grey;'>
        <p>© 2026 - MOHCINE EL HAKMAOUI & ANAS RIFAK</p>
        <p> 
        <a href="https://github.com/MOHCINE-ELHAKMAOUI" target="_blank">GitHub</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)