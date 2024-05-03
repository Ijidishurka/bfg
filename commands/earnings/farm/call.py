def calculate_gpu_cost(num_gpus):
    base_price = 500  # базовая стоимость первой видеокарты
    additional_percent = 0.15  # процент увеличения стоимости для каждой следующей видеокарты

    total_cost = base_price * (1 + additional_percent) ** (num_gpus - 1)

    return total_cost


def main():
    try:
        num_gpus = int(input("Введите количество видеокарт: "))
        if num_gpus < 1:
            raise ValueError("Количество видеокарт должно быть больше 0.")

        cost = calculate_gpu_cost(num_gpus)
        print(f"Общая стоимость {num_gpus} видеокарт: ${cost:.2f}")

    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
