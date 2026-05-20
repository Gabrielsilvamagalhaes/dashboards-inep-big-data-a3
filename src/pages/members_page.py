import streamlit as st

_MEMBERS = [
    {
        "name": "Gabriel Silva Magalhães",
        "ra": "1272313274",
        "github": "https://github.com/Gabrielsilvamagalhaes",
        "linkedin": "https://www.linkedin.com/in/gabriel-smagalhaes32/",
    },
    {
        "name": "Hanspeter Dietiker",
        "ra": "1272313332",
        "github": "https://github.com/hanspeterdietiker",
        "linkedin": "https://www.linkedin.com/in/hanspeterdietiker/",
    },
    {"name": "Alexandre"},
]

_PAGE_CSS = """
<style>
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.members-shell) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  .members-shell {
    max-width: 38rem;
    margin: 1.25rem auto 2rem;
    padding: 2.25rem 2rem 2rem;
    text-align: center;
    border-radius: 16px;
    background: linear-gradient(160deg, #1a2234 0%, #243049 45%, #1c2640 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow:
      0 18px 40px rgba(0, 0, 0, 0.35),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }
  .members-panel h3 {
    margin: 0 0 0.5rem;
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #ffffff;
  }
  .members-panel .members-accent {
    width: 3.5rem;
    height: 3px;
    margin: 0 auto 1.1rem;
    border-radius: 999px;
    background: linear-gradient(90deg, transparent, #7eb8ff, transparent);
  }
  .members-panel .members-subtitle {
    margin: 0 0 1.75rem;
    font-size: 0.98rem;
    color: rgba(255, 255, 255, 0.72);
    line-height: 1.5;
  }
  .member-divider {
    height: 1px;
    margin: 1.35rem auto;
    max-width: 85%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.22),
      transparent
    );
    border: none;
  }
  .member-card {
    padding: 0.65rem 0.75rem 0.35rem;
    border-radius: 12px;
    transition: background 0.2s ease;
  }
  .member-card:hover {
    background: rgba(255, 255, 255, 0.04);
  }
  .member-card h4 {
    margin: 0 0 0.45rem;
    font-size: 1.2rem;
    font-weight: 600;
    line-height: 1.4;
    color: #ffffff;
  }
  .member-card .member-ra {
    margin: 0 0 0.75rem;
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.88);
    letter-spacing: 0.02em;
  }
  .member-card .member-ra strong {
    font-weight: 600;
    color: #ffffff;
  }
  .member-links {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.25rem;
    flex-wrap: wrap;
    margin: 0;
  }
  .member-link {
    text-decoration: underline;
    text-underline-offset: 4px;
    text-decoration-color: rgba(255, 255, 255, 0.55);
    font-size: 0.92rem;
    font-weight: 500;
    color: #ffffff;
    transition: color 0.15s ease, text-decoration-color 0.15s ease;
  }
  .member-link:hover {
    color: #b8d9ff;
    text-decoration-color: #b8d9ff;
  }
  .member-link:focus-visible {
    outline: 2px solid #ffffff;
    outline-offset: 3px;
    border-radius: 2px;
  }
</style>
"""


def _member_card_html(
    name: str,
    ra: str | None = None,
    github: str | None = None,
    linkedin: str | None = None,
) -> str:
    ra_line = f'<p class="member-ra"><strong>RA:</strong> {ra}</p>' if ra else ""
    links: list[str] = []
    if github:
        links.append(
            f'<a class="member-link" href="{github}" target="_blank" '
            f'rel="noopener noreferrer">GitHub</a>'
        )
    if linkedin:
        links.append(
            f'<a class="member-link" href="{linkedin}" target="_blank" '
            f'rel="noopener noreferrer">LinkedIn</a>'
        )
    links_block = f'<p class="member-links">{" ".join(links)}</p>' if links else ""
    return (
        f'<article class="member-card" aria-label="Integrante {name}">'
        f"<h4>{name}</h4>{ra_line}{links_block}</article>"
    )


def membersPage():
    st.markdown(_PAGE_CSS, unsafe_allow_html=True)

    members_body = ""
    for index, member in enumerate(_MEMBERS):

        members_body += _member_card_html(**member)

    _, center, _ = st.columns([1, 2, 1])
    with center:
        with st.container():
            st.markdown(
                f"""
                <div class="members-shell">
                  <div class="members-panel">
                    <h3>Integrantes</h3>
                    <div class="members-accent"></div>
                    <p class="members-subtitle">Equipe do projeto Big Data A3</p>
                    {members_body}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
