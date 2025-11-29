"""
Create Sample Test Data for DOC Anomaly Detection System
Generates mock invoices and contracts for testing
"""

import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def create_sample_invoice(invoice_num, filename):
    """Create a sample invoice PDF"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 20))
    
    # Invoice details
    invoice_data = [
        ['Invoice Number:', f'INV-{invoice_num}'],
        ['Invoice Date:', datetime.now().strftime('%m/%d/%Y')],
        ['Due Date:', (datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y')],
        ['PO Number:', f'PO-{invoice_num.zfill(6)}'],
        ['Vendor:', 'TechCorp Solutions Inc.'],
        ['Bill To:', 'HP Enterprise Services']
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(invoice_table)
    story.append(Spacer(1, 30))
    
    # Line items
    story.append(Paragraph("Line Items", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    line_items = [
        ['Description', 'Quantity', 'Unit Price', 'Total'],
        ['Software License', '5', '$2,500.00', '$12,500.00'],
        ['Support Services', '12', '$500.00', '$6,000.00'],
        ['Implementation', '1', '$3,000.00', '$3,000.00']
    ]
    
    items_table = Table(line_items, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Total
    total_data = [
        ['Subtotal:', '$21,500.00'],
        ['Tax (8.5%):', '$1,827.50'],
        ['Total Amount:', '$23,327.50']
    ]
    
    total_table = Table(total_data, colWidths=[2*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
    ]))
    
    story.append(total_table)
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Payment Terms: Net 30 days", styles['Normal']))
    story.append(Paragraph("Thank you for your business!", styles['Normal']))
    
    doc.build(story)
    print(f"Created sample invoice: {filename}")

def create_sample_contract(contract_num, filename):
    """Create a sample contract PDF"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("SOFTWARE LEASE AGREEMENT", title_style))
    story.append(Spacer(1, 20))
    
    # Contract details
    contract_data = [
        ['Contract Number:', f'CONTRACT-{contract_num}'],
        ['Effective Date:', datetime.now().strftime('%m/%d/%Y')],
        ['Expiration Date:', (datetime.now() + timedelta(days=365)).strftime('%m/%d/%Y')],
        ['Lease Term:', '12 months'],
        ['Monthly Payment:', '$2,500.00'],
        ['Total Contract Value:', '$30,000.00'],
        ['Party 1:', 'HP Enterprise Services'],
        ['Party 2:', 'TechCorp Solutions Inc.']
    ]
    
    contract_table = Table(contract_data, colWidths=[2*inch, 3*inch])
    contract_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(contract_table)
    story.append(Spacer(1, 30))
    
    # Terms and conditions
    story.append(Paragraph("Terms and Conditions", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    terms = [
        "1. This agreement is for the lease of software licenses and related services.",
        "2. Monthly payments of $2,500.00 are due on the 1st of each month.",
        "3. The lease term is 12 months with automatic renewal unless terminated.",
        "4. Early termination requires 30 days written notice.",
        "5. Late payments are subject to a 1.5% monthly service charge.",
        "6. All intellectual property rights remain with the licensor.",
        "7. Support services are included as specified in Schedule A."
    ]
    
    for term in terms:
        story.append(Paragraph(term, styles['Normal']))
        story.append(Spacer(1, 8))
    
    # Payment schedule
    story.append(Spacer(1, 20))
    story.append(Paragraph("Payment Schedule", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    payment_data = [
        ['Payment Date', 'Amount', 'Status'],
        [(datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y'), '$2,500.00', 'Pending'],
        [(datetime.now() + timedelta(days=60)).strftime('%m/%d/%Y'), '$2,500.00', 'Pending'],
        [(datetime.now() + timedelta(days=90)).strftime('%m/%d/%Y'), '$2,500.00', 'Pending'],
        ['...', '...', '...'],
        [(datetime.now() + timedelta(days=365)).strftime('%m/%d/%Y'), '$2,500.00', 'Pending']
    ]
    
    payment_table = Table(payment_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(payment_table)
    
    # Signatures
    story.append(Spacer(1, 30))
    story.append(Paragraph("Signatures", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    sig_data = [
        ['HP Enterprise Services', 'TechCorp Solutions Inc.'],
        ['_________________________', '_________________________'],
        ['Signature', 'Signature'],
        ['_________________________', '_________________________'],
        ['Date', 'Date']
    ]
    
    sig_table = Table(sig_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(sig_table)
    
    doc.build(story)
    print(f"Created sample contract: {filename}")

def create_anomaly_invoice(invoice_num, filename):
    """Create an invoice with intentional anomalies for testing"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 20))
    
    # Invoice details with anomalies
    invoice_data = [
        ['Invoice Number:', f'INV-{invoice_num}'],
        ['Invoice Date:', (datetime.now() - timedelta(days=60)).strftime('%m/%d/%Y')],  # Old date
        ['Due Date:', (datetime.now() - timedelta(days=30)).strftime('%m/%d/%Y')],  # Past due
        ['PO Number:', f'PO-999999'],  # Different PO format
        ['Vendor:', 'TechCorp Solutions Inc.'],
        ['Bill To:', 'HP Enterprise Services']
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(invoice_table)
    story.append(Spacer(1, 30))
    
    # Line items with amount anomaly
    story.append(Paragraph("Line Items", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    line_items = [
        ['Description', 'Quantity', 'Unit Price', 'Total'],
        ['Software License', '5', '$2,500.00', '$12,500.00'],
        ['Support Services', '12', '$500.00', '$6,000.00'],
        ['Implementation', '1', '$3,000.00', '$3,000.00'],
        ['Additional Fees', '1', '$50,000.00', '$50,000.00']  # Unusually large amount
    ]
    
    items_table = Table(line_items, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Total with anomaly
    total_data = [
        ['Subtotal:', '$71,500.00'],
        ['Tax (8.5%):', '$6,077.50'],
        ['Total Amount:', '$77,577.50']
    ]
    
    total_table = Table(total_data, colWidths=[2*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
    ]))
    
    story.append(total_table)
    
    doc.build(story)
    print(f"Created anomaly invoice: {filename}")

def main():
    """Create all sample documents"""
    # Create sample data directory
    sample_dir = "sample_data"
    os.makedirs(sample_dir, exist_ok=True)
    
    print("Creating sample test data for DOC Anomaly Detection System...")
    
    # Create normal invoices
    create_sample_invoice("001", f"{sample_dir}/invoice_001_normal.pdf")
    create_sample_invoice("002", f"{sample_dir}/invoice_002_normal.pdf")
    
    # Create normal contracts
    create_sample_contract("001", f"{sample_dir}/contract_001_normal.pdf")
    create_sample_contract("002", f"{sample_dir}/contract_002_normal.pdf")
    
    # Create invoices with anomalies
    create_anomaly_invoice("003", f"{sample_dir}/invoice_003_anomalies.pdf")
    
    print(f"\nSample data created in '{sample_dir}' directory:")
    print("- invoice_001_normal.pdf (Normal invoice)")
    print("- invoice_002_normal.pdf (Normal invoice)")
    print("- contract_001_normal.pdf (Normal contract)")
    print("- contract_002_normal.pdf (Normal contract)")
    print("- invoice_003_anomalies.pdf (Invoice with anomalies)")
    print("\nYou can now test the system with these sample documents!")

if __name__ == "__main__":
    main()

