from datetime import datetime

def validate_convert_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")  # formato "DD/MM/YYYY"
        return dt.strftime('%Y-%m-%d')
    except ValueError as e:
        # Parse the error message to determine the issue
        error_msg = str(e)
        if "does not match format" in error_msg:
            raise ValueError(f"Formato incorreto. Use DD/MM/YYYY (ex: 31/12/2024)") from None
        elif "day is out of range" in error_msg or "month is out of range" in error_msg:
            raise ValueError(f"Data inválida: {date_str} (dia/mês fora do limite)") from None
        else:
            raise ValueError(f"Data inválida: {date_str}") from None