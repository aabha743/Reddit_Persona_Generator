from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os

def generate_pdf(username, persona_text):
    try:
        # Ensure the personas directory exists
        os.makedirs('data/personas', exist_ok=True)
        
        # Set up the document
        output_path = os.path.abspath(f'data/personas/{username}_persona.pdf')
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Create styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            textColor=colors.HexColor('#333333'),
            spaceAfter=30
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            textColor=colors.HexColor('#ff4500'),
            spaceAfter=12
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        )
        quote_style = ParagraphStyle(
            'CustomQuote',
            parent=styles['Italic'],
            textColor=colors.HexColor('#666666'),
            leftIndent=20,
            spaceAfter=12
        )
        
        # Build the document content
        story = []
        
        # Add title
        story.append(Paragraph('Reddit User Persona', title_style))
        story.append(Paragraph(f'u/{username}', heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Process persona sections
        sections = persona_text.split('\n\n')
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                
                # Add section title
                story.append(Paragraph(title.strip(), heading_style))
                
                # Handle different section types
                if title.strip() == 'QUOTE':
                    story.append(Paragraph(f'"{content.strip()}"', quote_style))
                elif title.strip() == 'MOTIVATIONS':
                    # Process motivation ratings
                    for line in content.strip().split('\n'):
                        if ':' in line:
                            motivation, rating = line.split(':', 1)
                            story.append(Paragraph(
                                f'{motivation.strip()}: {rating.strip()}/5',
                                normal_style
                            ))
                else:
                    story.append(Paragraph(content.strip(), normal_style))
                
                story.append(Spacer(1, 0.1*inch))
        
        # Build the PDF
        doc.build(story)
        
        print(f"PDF successfully generated at: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        try:
            # Create a simple fallback PDF
            c = canvas.Canvas(output_path, pagesize=letter)
            c.setFont('Helvetica-Bold', 16)
            c.drawString(72, 800, f'Persona for u/{username}')
            
            c.setFont('Helvetica', 12)
            y = 750
            for line in persona_text.split('\n'):
                if y > 72:  # Ensure we don't write below the bottom margin
                    c.drawString(72, y, line)
                    y -= 15
                    
            c.save()
            print("Fallback PDF generated successfully")
            return output_path
            
        except Exception as fallback_error:
            print(f"Error generating fallback PDF: {str(fallback_error)}")
            raise
