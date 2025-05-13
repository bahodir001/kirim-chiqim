import io
import xlsxwriter
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from income.models import Income
from expenses.models import Expense
from datetime import datetime

class ExportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        y = 800
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Kirim va Chiqim Hisoboti")
        y -= 40

        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 30

        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)

        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Kirimlar:")
        y -= 20
        p.setFont("Helvetica", 10)
        for income in incomes:
            if y < 50:
                p.showPage()
                y = 800
            p.drawString(100, y, f"{income.date} - {income.income_type} - {income.amount} - {income.method}")
            y -= 15

        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Chiqimlar:")
        y -= 20
        p.setFont("Helvetica", 10)
        for expense in expenses:
            if y < 50:
                p.showPage()
                y = 800
            p.drawString(100, y, f"{expense.date} - {expense.expense_type} - {expense.amount} - {expense.method}")
            y -= 15

        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


class ExportExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        income_sheet = workbook.add_worksheet('Kirimlar')
        expense_sheet = workbook.add_worksheet('Chiqimlar')

        income_sheet.write_row(0, 0, ['Sana', 'Turi', 'Summasi', 'Shakli'])
        expense_sheet.write_row(0, 0, ['Sana', 'Turi', 'Summasi', 'Shakli'])

        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)

        for idx, income in enumerate(incomes, start=1):
            income_sheet.write_row(idx, 0, [str(income.date), income.income_type, float(income.amount), income.method])

        for idx, expense in enumerate(expenses, start=1):
            expense_sheet.write_row(idx, 0, [str(expense.date), expense.expense_type, float(expense.amount), expense.method])

        workbook.close()
        output.seek(0)
        response.write(output.read())
        return response
