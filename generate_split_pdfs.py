import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7F8C8D"))
        self.drawString(54, 36, "Confidential - LocalBuka Recruiting")
        self.drawRightString(558, 36, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf(filename, title, track_name, description, req_paragraphs, question_paragraphs, rubric_rows):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor("#E67E22"), spaceAfter=5)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor("#2C3E50"), spaceAfter=15)
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor("#2C3E50"), spaceBefore=12, spaceAfter=8, keepWithNext=True)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#E67E22"), spaceBefore=8, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#34495E"), spaceAfter=6)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#34495E"), leftIndent=15, firstLineIndent=-10, spaceAfter=4)
    meta_label = ParagraphStyle('ML', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor("#2C3E50"))
    meta_val = ParagraphStyle('MV', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#34495E"))

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(f"Track: {track_name}", subtitle_style))
    
    info_data = [
        [Paragraph("Time Limit:", meta_label), Paragraph("3-5 Days (Take-Home)", meta_val)],
        [Paragraph("Target Level:", meta_label), Paragraph("Software Engineering Intern (Calibrated Scope)", meta_val)],
        [Paragraph("Submission:", meta_label), Paragraph("Email your public GitHub repository link and a 2-minute walkthrough video to <b>hellohr@localbuka.com</b>", meta_val)]
    ]
    t_info = Table(info_data, colWidths=[100, 404])
    t_info.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#ECF0F1")),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Product Context", h1_style))
    story.append(Paragraph(description, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Practical Requirements", h1_style))
    for p in req_paragraphs:
        if p.startswith("•"):
            story.append(Paragraph(p, bullet_style))
        else:
            story.append(Paragraph(p, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Technical Assessment Questions", h1_style))
    for title_q, desc_q in question_paragraphs:
        story.append(Paragraph(title_q, h2_style))
        story.append(Paragraph(desc_q, body_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())
    story.append(Paragraph("Evaluation Rubric", h1_style))
    story.append(Paragraph("Your submission will be scored out of 100 points based on the following breakdown:", body_style))
    
    rubric_rows.insert(0, [Paragraph("<b>Criteria</b>", meta_label), Paragraph("<b>Weight</b>", meta_label), Paragraph("<b>Description</b>", meta_label)])
    t_rubric = Table(rubric_rows, colWidths=[140, 70, 294])
    t_rubric.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ECF0F1")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#ECF0F1")),
    ]))
    story.append(t_rubric)
    
    doc.build(story, canvasmaker=NumberedCanvas)

# --- BACKEND TRACK ---
backend_desc = (
    "LocalBuka connects customers to local food vendors (bukas) in Nigeria. "
    "For the Backend Intern track, you will build a clean, type-safe REST API using NestJS (or Node.js/Express) and TypeScript. "
    "You do not need to build any user interface. Focus entirely on clean routing, database queries, logic validation, and error handling."
)
backend_reqs = [
    "You will implement 4 core REST endpoints based on our provided schema and mock data:",
    "• <b>GET /restaurants</b>: List all restaurants. Implement basic search by restaurant name. If query params <code>latitude</code> and <code>longitude</code> are provided, return the restaurants sorted by distance (closest first).",
    "• <b>GET /restaurants/:id</b>: Fetch detailed info on a single restaurant, including its reviews.",
    "• <b>POST /restaurants/:id/reviews</b>: Add a new review (rating scale 1-5). Ensure a user can only review the same restaurant once.",
    "• <b>POST /points/earn</b>: Awards points for a <code>check-in</code> (50 pts) or <code>review</code> (20 pts). Restrict check-ins to once per user per restaurant per calendar day.",
    "• <b>GET /points/balance/:userId</b>: Fetch current total points and points transaction ledger."
]
backend_qs = [
    ("Q1. TypeScript Data Shape Parsing", 
     "Write a parser function <code>parseRestaurant(raw: unknown): Restaurant</code> in TypeScript. It must cast raw incoming snake_case fields or string numbers into correct types, throwing a validation error if required fields are missing."),
    ("Q2. Handling Race Conditions",
     "Describe how you would prevent race conditions if a user sends multiple concurrent points redemption requests at the exact same millisecond. Propose one database level lock strategy.")
]
backend_rubric = [
    [Paragraph("API Endpoint Functionality", ParagraphStyle('R1')), Paragraph("35 pts", ParagraphStyle('R2')), Paragraph("All endpoints work, return exact JSON schemas, and handle status codes correctly.", ParagraphStyle('R3'))],
    [Paragraph("Business Logic & Constraints", ParagraphStyle('R1')), Paragraph("25 pts", ParagraphStyle('R2')), Paragraph("Correctly blocks duplicate reviews and restricts check-ins to once per day.", ParagraphStyle('R3'))],
    [Paragraph("Database & Geolocation Math", ParagraphStyle('R1')), Paragraph("20 pts", ParagraphStyle('R2')), Paragraph("Calculates distances using coordinates and orders list correctly.", ParagraphStyle('R3'))],
    [Paragraph("TypeScript & Code Hygiene", ParagraphStyle('R1')), Paragraph("20 pts", ParagraphStyle('R2')), Paragraph("Strict typings used, proper NestJS modules, no raw 'any' types.", ParagraphStyle('R3'))],
]

# --- FRONTEND TRACK ---
frontend_desc = (
    "For the Frontend Intern track, you will build a clean, responsive web dashboard using React and TypeScript. "
    "You will connect to mock local endpoints (or write standard mock APIs directly inside the frontend) to present a smooth user experience. "
    "We are looking for functional flow, component composition, state handling, and attention to visual detail."
)
frontend_reqs = [
    "You will build 2 main pages/views in React:",
    "• <b>Buka Discovery Dashboard</b>: Render a grid of restaurant cards. Implement filters for Cuisine type and Rating. Show a visual skeleton loader while data is loading.",
    "• <b>Restaurant Cards</b>: Show details, photos, and tags. Include a 'Save/Favorite' button implementing optimistic state updates (instantly highlights on click, and reverts with an alert if the API call fails).",
    "• <b>Points & Rewards Panel</b>: Displays the user's mock points balance and lists the recent transaction history ledger."
]
frontend_qs = [
    ("Q1. Optimistic UI Updates & Error Recovery",
     "Explain how you implemented the optimistic favorite toggle. Provide a code sample showing how you handle rolling back state in case the API request fails."),
    ("Q2. React Component Optimization",
     "Suppose the restaurant listing renders 200+ cards, causing scrolling lag. Name 2 React strategies or techniques you would use to optimize rendering performance.")
]
frontend_rubric = [
    [Paragraph("UI Completeness & Aesthetics", ParagraphStyle('R1')), Paragraph("35 pts", ParagraphStyle('R2')), Paragraph("Responsive layout, clean color palette, modern cards matching LocalBuka branding.", ParagraphStyle('R3'))],
    [Paragraph("State Management & Rollbacks", ParagraphStyle('R1')), Paragraph("25 pts", ParagraphStyle('R2')), Paragraph("Optimistic UI state updates successfully and rolls back cleanly on network failures.", ParagraphStyle('R3'))],
    [Paragraph("Loading & Empty States", ParagraphStyle('R1')), Paragraph("20 pts", ParagraphStyle('R2')), Paragraph("Skeleton loaders present and handles empty search results nicely.", ParagraphStyle('R3'))],
    [Paragraph("TypeScript & Code Quality", ParagraphStyle('R1')), Paragraph("20 pts", ParagraphStyle('R2')), Paragraph("Props typed strictly, reusable component design, clean folder structure.", ParagraphStyle('R3'))],
]

if __name__ == "__main__":
    build_pdf("/Users/mac/Documents/assessment-repo/LocalBuka_Backend_Intern_Assessment.pdf", "LocalBuka Intern Assessment", "Backend Engineering", backend_desc, backend_reqs, backend_qs, backend_rubric)
    build_pdf("/Users/mac/Documents/assessment-repo/LocalBuka_Frontend_Intern_Assessment.pdf", "LocalBuka Intern Assessment", "Frontend Engineering", frontend_desc, frontend_reqs, frontend_qs, frontend_rubric)
    print("Backend and Frontend PDFs generated successfully.")
