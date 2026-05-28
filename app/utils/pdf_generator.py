import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,HRFlowable,)
from reportlab.lib.styles import (getSampleStyleSheet,ParagraphStyle,)
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


class PDFInvoiceService:

    @staticmethod
    def generate_invoice_pdf(invoice):

        os.makedirs("media/invoices", exist_ok=True)

        file_path = (
            f"media/invoices/"
            f"{invoice.invoice_number}.pdf"
        )

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.6 * inch,
            leftMargin=0.6 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch,
        )

        BRAND   = colors.HexColor("#1A73E8")
        DARK    = colors.HexColor("#1F2937")
        MUTED   = colors.HexColor("#6B7280")
        LIGHT   = colors.HexColor("#F3F4F6")
        SUCCESS = colors.HexColor("#10B981")
        WHITE   = colors.white

        base = getSampleStyleSheet()

        _prefix = f"inv_{invoice.invoice_number}_"

        def style(name, **kw):
            return ParagraphStyle(
                _prefix + name,
                parent=base["Normal"],
                **kw,
            )

        s_title = style(
            "Title",
            fontSize=22,
            textColor=WHITE,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            spaceAfter=0,
        )

        s_subtitle = style(
            "Sub",
            fontSize=9,
            textColor=WHITE,
            alignment=TA_CENTER,
            fontName="Helvetica",
        )

        s_section = style(
            "Section",
            fontSize=11,
            textColor=BRAND,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=4,
        )

        s_label = style(
            "Label",
            fontSize=9,
            textColor=MUTED,
            fontName="Helvetica",
        )

        s_value = style(
            "Value",
            fontSize=10,
            textColor=DARK,
            fontName="Helvetica-Bold",
        )

        s_total = style(
            "Total",
            fontSize=13,
            textColor=WHITE,
            fontName="Helvetica-Bold",
            alignment=TA_RIGHT,
        )

        s_footer = style(
            "Footer",
            fontSize=9,
            textColor=MUTED,
            alignment=TA_CENTER,
            fontName="Helvetica-Oblique",
        )

        def INR(amount):
            """Format a monetary amount. Guards against None values."""
            return f"Rs. {amount if amount is not None else '0.00'}"

        customer_name = (
            invoice.customer.full_name
            if invoice.customer
            else "N/A"
        )

        driver_name = (
            invoice.driver.user.full_name
            if invoice.driver and invoice.driver.user
            else "N/A"
        )

        vehicle_number = (
            invoice.vehicle.vehicle_number
            if invoice.vehicle
            else "N/A"
        )

        story = []



        header_data = [[Paragraph("E-BILL INVOICE", s_title)]]

        header = Table(header_data, colWidths=[7.3 * inch])
        header.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), BRAND),
            ("TOPPADDING",    (0, 0), (-1, -1), 18),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ]))

        story.append(header)


        inv_row = [[
            Paragraph(
                f"Invoice #{invoice.invoice_number}"
                f" | {invoice.trip_type.value}",
                s_subtitle,
            )
        ]]

        inv_banner = Table(inv_row, colWidths=[7.3 * inch])
        inv_banner.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), DARK),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(inv_banner)
        story.append(Spacer(1, 14))


        story.append(Paragraph("TRIP DETAILS", s_section))

        trip_data = [
            [
                Paragraph("Customer", s_label),
                Paragraph(customer_name, s_value),
                Paragraph("Driver", s_label),
                Paragraph(driver_name, s_value),
            ],
            [
                Paragraph("Vehicle", s_label),
                Paragraph(vehicle_number, s_value),
                Paragraph("Trip Type", s_label),
                Paragraph(invoice.trip_type.value, s_value),
            ],
        ]

        trip_table = Table(
            trip_data,
            colWidths=[1.1 * inch, 2.55 * inch, 1.1 * inch, 2.55 * inch],
        )
        trip_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), LIGHT),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))

        story.append(trip_table)
        story.append(Spacer(1, 14))


        story.append(Paragraph("FARE BREAKDOWN", s_section))

        fare_rows = [
            ("Base Fare",                          INR(invoice.base_fare)),
            (f"Distance ({invoice.distance_km} km)", INR(invoice.distance_charge)),
            ("Time Charge",                        INR(invoice.time_charge)),
            ("Waiting Charge",                     INR(invoice.waiting_charge)),
            ("Surge Charge",                       INR(invoice.surge_charge)),
            ("Tax",                                INR(invoice.tax_amount)),
            ("Discount",                           f"- {INR(invoice.discount_amount)}"),
        ]

        s_amount_normal   = style("AmtNormal",   fontSize=10, textColor=DARK,    fontName="Helvetica-Bold", alignment=TA_RIGHT)
        s_amount_discount = style("AmtDiscount", fontSize=10, textColor=SUCCESS,  fontName="Helvetica-Bold", alignment=TA_RIGHT)

        fare_style_rows = [
            [
                Paragraph(label, s_label),
                Paragraph(value, s_amount_discount if label == "Discount" else s_amount_normal),
            ]
            for label, value in fare_rows
        ]

        fare_table = Table(fare_style_rows, colWidths=[5 * inch, 2.3 * inch])
        fare_table.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT, WHITE]),
            ("GRID",           (0, 0), (-1, -1), 0.4, colors.HexColor("#E5E7EB")),
            ("TOPPADDING",     (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 7),
            ("LEFTPADDING",    (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",   (0, 0), (-1, -1), 10),
        ]))

        story.append(fare_table)


        s_total_label = style(
            "TotalLabel",
            fontSize=12,
            textColor=WHITE,
            fontName="Helvetica-Bold",
        )

        total_data = [[
            Paragraph("TOTAL AMOUNT", s_total_label),
            Paragraph(INR(invoice.total_amount), s_total),
        ]]

        total_table = Table(total_data, colWidths=[5 * inch, 2.3 * inch])
        total_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), BRAND),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ]))

        story.append(total_table)
        story.append(Spacer(1, 14))


        story.append(Paragraph("PAYMENT DETAILS", s_section))

        status_value = invoice.payment_status.value
        status_colour = (
            SUCCESS
            if status_value.lower() == "paid"
            else colors.HexColor("#EF4444")
        )

        s_status = style(
            "PayStatus",
            fontSize=10,
            textColor=status_colour,
            fontName="Helvetica-Bold",
        )

        pay_data = [[
            Paragraph("Payment Method", s_label),
            Paragraph(str(invoice.payment_method), s_value),
            Paragraph("Payment Status", s_label),
            Paragraph(status_value, s_status),
        ]]

        pay_table = Table(
            pay_data,
            colWidths=[1.4 * inch, 2.25 * inch, 1.4 * inch, 2.25 * inch],
        )
        pay_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), LIGHT),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("TOPPADDING",    (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))

        story.append(pay_table)
        story.append(Spacer(1, 20))


        story.append(
            HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor("#D1D5DB"),
            )
        )

        story.append(Spacer(1, 8))

        story.append(
            Paragraph("Thank you for riding with us!", s_footer)
        )

        doc.build(story)

        return file_path
