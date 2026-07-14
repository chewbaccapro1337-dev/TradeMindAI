from risk import calculate_risk


def main():
    print("=== TradeMind AI ===")

    balance = float(input("Введите баланс ($): "))
    risk_percent = float(input("Введите риск (%): "))

    risk = calculate_risk(balance, risk_percent)

    print(f"\nМаксимальный риск: ${risk:.2f}")


if __name__ == "__main__":
    main()