import os

from reportlab.lib.pagesizes import letter

from reportlab.pdfgen import canvas


class PDFInvoiceService:

    @staticmethod
    def generate_invoice_pdf(invoice):

        # ============================================
        # CREATE INVOICE FOLDER
        # ============================================

        os.makedirs(
            "media/invoices",
            exist_ok=True
        )

        # ============================================
        # FILE PATH
        # ============================================

        file_path = (

            f"media/invoices/"
            f"{invoice.invoice_number}.pdf"

        )

        # ============================================
        # CREATE PDF
        # ============================================

        pdf = canvas.Canvas(
            file_path,
            pagesize=letter
        )

        width, height = letter

        # ============================================
        # TITLE
        # ============================================

        pdf.setFont(
            "Helvetica-Bold",
            22
        )

        pdf.drawString(
            180,
            760,
            "E-BILL INVOICE"
        )

        # ============================================
        # LINE
        # ============================================

        pdf.line(
            50,
            740,
            550,
            740
        )

        # ============================================
        # CUSTOMER / DRIVER DETAILS
        # ============================================

        customer_name = (

            invoice.customer.full_name

            if invoice.customer

            else "N/A"

        )

        driver_name = (

            invoice.driver.user.full_name

            if invoice.driver
            and invoice.driver.user

            else "N/A"

        )

        vehicle_number = (

            invoice.vehicle.vehicle_number

            if invoice.vehicle

            else "N/A"

        )

        # ============================================
        # BASIC DETAILS
        # ============================================

        pdf.setFont(
            "Helvetica",
            12
        )

        y = 700

        pdf.drawString(
            50,
            y,
            f"Invoice Number : "
            f"{invoice.invoice_number}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Trip ID : "
            f"{invoice.trip_id}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Trip Type : "
            f"{invoice.trip_type.value}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Customer Name : "
            f"{customer_name}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Driver Name : "
            f"{driver_name}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Vehicle Number : "
            f"{vehicle_number}"
        )

        y -= 40

        # ============================================
        # FARE DETAILS TITLE
        # ============================================

        pdf.setFont(
            "Helvetica-Bold",
            15
        )

        pdf.drawString(
            50,
            y,
            "Fare Details"
        )

        y -= 30

        # ============================================
        # FARE DETAILS
        # ============================================

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            50,
            y,
            f"Base Fare : "
            f"₹{invoice.base_fare}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Distance : "
            f"{invoice.distance_km} KM"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Distance Charge : "
            f"₹{invoice.distance_charge}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Time Charge : "
            f"₹{invoice.time_charge}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Waiting Charge : "
            f"₹{invoice.waiting_charge}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Surge Charge : "
            f"₹{invoice.surge_charge}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Tax Amount : "
            f"₹{invoice.tax_amount}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Discount : "
            f"₹{invoice.discount_amount}"
        )

        y -= 35

        # ============================================
        # TOTAL AMOUNT
        # ============================================

        pdf.setFont(
            "Helvetica-Bold",
            17
        )

        pdf.drawString(
            50,
            y,
            f"Total Amount : "
            f"₹{invoice.total_amount}"
        )

        y -= 45

        # ============================================
        # PAYMENT DETAILS
        # ============================================

        pdf.setFont(
            "Helvetica-Bold",
            15
        )

        pdf.drawString(
            50,
            y,
            "Payment Details"
        )

        y -= 30

        pdf.setFont(
            "Helvetica",
            12
        )

        pdf.drawString(
            50,
            y,
            f"Payment Method : "
            f"{invoice.payment_method}"
        )

        y -= 25

        pdf.drawString(
            50,
            y,
            f"Payment Status : "
            f"{invoice.payment_status.value}"
        )

        y -= 50

        # ============================================
        # FOOTER
        # ============================================

        pdf.line(
            50,
            y,
            550,
            y
        )

        y -= 30

        pdf.setFont(
            "Helvetica-Oblique",
            11
        )

        pdf.drawString(
            120,
            y,
            "Thank you for riding with us!"
        )

        # ============================================
        # SAVE PDF
        # ============================================

        pdf.save()

        return file_path