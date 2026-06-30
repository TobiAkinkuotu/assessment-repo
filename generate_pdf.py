import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
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
        
        # Header (Only on page 2 and later)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#2C3E50"))
            self.drawString(54, 755, "LOCALBUKA ENGINEERING INTERN CASE STUDY & TECHNICAL ASSESSMENT")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7F8C8D"))
        self.drawString(54, 36, "Confidential - LocalBuka Recruiting")
        self.drawRightString(558, 36, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def create_case_study_pdf(filename):
    # Set up document margins (0.75 inch = 54 pt)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#E67E22"), # LocalBuka Orange
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#7F8C8D"),
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2C3E50"),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#E67E22"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#34495E"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#34495E"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#2C3E50"),
        backColor=colors.HexColor("#ECF0F1"),
        borderColor=colors.HexColor("#BDC3C7"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=5,
        spaceAfter=5
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2C3E50")
    )
    
    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#34495E")
    )

    story = []

    # 1. HEADER / TITLE BLOCK
    story.append(Paragraph("LocalBuka Engineering Intern", title_style))
    story.append(Paragraph("Technical Assessment & Full-Stack Case Study", ParagraphStyle('CoverTitle2', parent=title_style, fontSize=18, leading=22, textColor=colors.HexColor("#2C3E50"))))
    story.append(Paragraph("A practical evaluation package tailored to LocalBuka's core ecosystem", subtitle_style))
    story.append(Spacer(1, 10))

    # Info Grid table
    info_data = [
        [Paragraph("Target Role:", meta_label_style), Paragraph("Software Engineering Intern (React, React Native, NestJS)", meta_val_style)],
        [Paragraph("Time Limit:", meta_label_style), Paragraph("5 Days (Take-Home)", meta_val_style)],
        [Paragraph("Evaluation Focus:", meta_label_style), Paragraph("Functional Completeness, TypeScript rigor, API Design, Mobile GPS Integration, Clean Git history", meta_val_style)],
        [Paragraph("Submission Channel:", meta_label_style), Paragraph("Send your GitHub repository link and walkthrough video to <b>hellohr@localbuka.com</b>", meta_val_style)]
    ]
    t_info = Table(info_data, colWidths=[120, 384])
    t_info.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#ECF0F1")),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 20))

    # 2. PRODUCT CONTEXT
    story.append(Paragraph("1. The Product Context", h1_style))
    story.append(Paragraph(
        "LocalBuka is a Nigerian restaurant discovery platform connecting hungry users with top chefs, neighborhood bukas, and premium dining spots. "
        "To test your ability to work on our production code, you will implement a lightweight prototype comprising parts of three core features:",
        body_style
    ))
    story.append(Paragraph("• <b>Restaurant Discovery Feed</b>: Users can view nearby bukas, search by name, and filter by cuisine type, price, or rating.", bullet_style))
    story.append(Paragraph("• <b>Points & Rewards</b>: A gamified user engagement loop where users earn points for checks-ins or reviews, and redeem them for monetary vouchers.", bullet_style))
    story.append(Paragraph("• <b>GPS check-in</b>: Mobile users can verify physical presence at a restaurant within 100 meters to claim daily bonus points.", bullet_style))
    story.append(Spacer(1, 15))

    # 3. BACKEND REQUIREMENTS
    story.append(Paragraph("2. Backend API Requirements (NestJS / Express)", h1_style))
    story.append(Paragraph("Your server must expose a set of clean, validated REST endpoints with consistent JSON payloads:", body_style))
    
    story.append(Paragraph("• <b>GET /restaurants</b>: List and search restaurants. If query parameters <i>latitude</i> and <i>longitude</i> are provided, calculate the distance in kilometers using the Haversine formula and return the list sorted from closest to furthest. Support filtering by <i>cuisine</i>, <i>priceRange</i> (1 to 4), and <i>minRating</i>.", bullet_style))
    story.append(Paragraph("• <b>GET /restaurants/:id</b>: Fetch detailed info on a single restaurant, including a child array of reviews.", bullet_style))
    story.append(Paragraph("• <b>POST /restaurants/:id/reviews</b>: Add a user review. Input must be validated (rating must be an integer between 1 and 5). <i>Crucial Constraint</i>: A user cannot review the same restaurant more than once; handle this conflict and return a descriptive error.", bullet_style))
    story.append(Paragraph("• <b>POST /points/earn</b>: Awards points to a user. Actions supported are <i>check-in</i> (50 pts), <i>review</i> (20 pts), and <i>referral</i> (100 pts). Ensure check-ins are restricted to once per calendar day per restaurant.", bullet_style))
    story.append(Paragraph("• <b>POST /points/redeem</b>: Redeems user points. Must validate that the user has a sufficient balance and that redemptions are performed in multiples of 50 points (e.g., 50 pts = N500 off).", bullet_style))
    story.append(Paragraph("• <b>GET /points/balance/:userId</b>: Returns the current aggregate points balance and a chronological transaction ledger of points earned and redeemed.", bullet_style))
    story.append(Spacer(1, 15))

    # 4. FRONTEND REQUIREMENTS
    story.append(Paragraph("3. Frontend Web Requirements (React)", h1_style))
    story.append(Paragraph("Build a responsive web application that interacts with your backend API. It should include:", body_style))
    story.append(Paragraph("• <b>Discovery Dashboard</b>: A list or grid of restaurant cards with search and filter controls. Implement skeletons/spinners for loading states.", bullet_style))
    story.append(Paragraph("• <b>Optimistic Favorites Toggle</b>: A button on the restaurant card to save/favorite it. The UI state must update immediately before the network request completes. If the request fails, the state must roll back gracefully and alert the user.", bullet_style))
    story.append(Paragraph("• <b>Voucher & Rewards Dashboard</b>: Displays user points and lists the ledger. Include a working voucher redemption section.", bullet_style))
    story.append(Spacer(1, 15))

    # 5. MOBILE REQUIREMENTS
    story.append(Paragraph("4. Mobile Screen Requirements (React Native) [Optional but Preferred]", h1_style))
    story.append(Paragraph("Develop a simple React Native app screen using Expo or React Native CLI representing the <b>Restaurant Detail & Check-In</b> flow:", body_style))
    story.append(Paragraph("• Render the restaurant name, cuisine, rating, and a <b>'Check-In to Earn Points'</b> button.", bullet_style))
    story.append(Paragraph("• When tapped, request device location permissions. If granted, fetch the current GPS coordinates of the device.", bullet_style))
    story.append(Paragraph("• Compare the coordinates with the restaurant's location. If the user is within 100 meters, post to the backend `/points/earn` check-in endpoint and display a success status animation. Otherwise, prompt the user that they are too far away.", bullet_style))
    story.append(Spacer(1, 15))

    story.append(PageBreak())

    # 6. PRACTICAL IMPLEMENTATION QUESTIONS
    story.append(Paragraph("5. Technical Assessment Questions", h1_style))
    story.append(Paragraph(
        "To test your understanding of core technologies, complete the following practical coding tasks and include the answers in your <b>SOLUTION.md</b>:",
        body_style
    ))
    
    story.append(Paragraph("Q1. TypeScript & API Response Validation", h2_style))
    story.append(Paragraph(
        "Often raw JSON data returned from upstream or legacy endpoints contains inconsistent snake_case keys or string-formatted floats instead of numbers. "
        "Define a strict TypeScript type or interface representing the ideal <b>Restaurant</b> structure. Write a type-safe parser function "
        "<code>parseRestaurant(raw: unknown): Restaurant</code> that parses, casts, and validates raw payloads, throwing clear errors on missing fields or incorrect types. "
        "How would you integrate this with NestJS's global ValidationPipe using <i>class-validator</i> and <i>class-transformer</i>?",
        body_style
    ))
    
    story.append(Paragraph("Q2. Concurrent Promises & Graceful Timeouts", h2_style))
    story.append(Paragraph(
        "To maximize search availability, we want to query our local database API and a fallback Google Places API simultaneously. "
        "Write a clean JavaScript/TypeScript utility function <code>fetchNearbyRestaurants(coords)</code> using Promise APIs that starts both requests concurrently. "
        "If the local database responds first, use it. If the local database fails, fallback to Google Places. "
        "Enforce a strict global timeout of 5000ms. If both fail or the timeout triggers, return a safe empty list and log the error context.",
        body_style
    ))

    story.append(Paragraph("Q3. Race Conditions in Points Redemption", h2_style))
    story.append(Paragraph(
        "If a user rapidly taps the 'Redeem Voucher' button, there is a risk of a race condition where multiple requests arrive at the backend "
        "before the database can update the points ledger, potentially leading to double-redemption (spending more points than available). "
        "Describe two distinct approaches (one database-level, one API/service-level) to safely prevent race conditions in points balance checks.",
        body_style
    ))

    story.append(Paragraph("Q4. React Performance & Component Rendering", h2_style))
    story.append(Paragraph(
        "In our search results page, rendering 200+ restaurant cards can cause severe UI lag on lower-end mobile devices during scrolling or filtering. "
        "Detail 3 specific optimization strategies you would apply to the React component tree (e.g. virtualization, memoization) to keep rendering smooth. "
        "How would you measure the performance improvements using browser DevTools?",
        body_style
    ))

    story.append(Spacer(1, 15))

    # 7. EVALUATION RUBRIC PREVIEW
    story.append(Paragraph("6. Grading & Evaluation Rubric", h1_style))
    story.append(Paragraph("Candidates will be assessed out of 100 points, broken down as follows:", body_style))
    
    rubric_headers = [
        Paragraph("<b>Category</b>", meta_label_style),
        Paragraph("<b>Weight</b>", meta_label_style),
        Paragraph("<b>Core Grading Criteria</b>", meta_label_style)
    ]
    rubric_rows = [
        rubric_headers,
        [Paragraph("Backend API (NestJS)", body_style), Paragraph("40 Points", body_style), Paragraph("REST standards, schema design, index usage, input validation, daily duplicate check constraints.", body_style)],
        [Paragraph("Frontend App (React)", body_style), Paragraph("30 Points", body_style), Paragraph("State management choice, design aesthetics, responsive design, optimistic UI states with error recovery.", body_style)],
        [Paragraph("Mobile App (React Native)", body_style), Paragraph("15 Points", body_style), Paragraph("Permission Handling, GPS coordinates math, check-in validation, deep linking setup.", body_style)],
        [Paragraph("Engineering Quality", body_style), Paragraph("15 Points", body_style), Paragraph("TypeScript strictness (avoiding 'any'), clean Git commits, README accuracy, SOLUTION.md writeup.", body_style)]
    ]
    
    t_rubric = Table(rubric_rows, colWidths=[130, 80, 294])
    t_rubric.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#ECF0F1")),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#ECF0F1")),
    ]))
    story.append(t_rubric)
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    create_case_study_pdf("/Users/mac/Documents/assessment-repo/LocalBuka_Intern_Case_Study.pdf")
    print("PDF Generated successfully.")
