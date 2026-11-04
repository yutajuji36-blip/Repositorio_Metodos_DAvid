import unicodedata


def calcular_media(datos):
    """Recibe una lista de números y devuelve su media aritmética."""
    if not datos:
        raise ValueError("La lista está vacía, no se puede calcular la media.")
    return sum(datos) / len(datos)


def suma_cuadrados(x, media_x):
    """Calcula Σ(X - X̄)²"""
    suma = 0
    for xi in x:
        suma += (xi - media_x) ** 2
    return suma


def suma_productos(x, y, media_x, media_y):
    """Calcula Σ(X - X̄)(Y - Ȳ)"""
    suma = 0
    for xi, yi in zip(x, y):
        suma += (xi - media_x) * (yi - media_y)
    return suma


def pedir_datos(nombre):
    """Pide los valores de una variable en una sola línea separados por comas."""
    while True:
        entrada = input(f"Ingresa los valores de {nombre} separados por comas: ").strip()
        if entrada == "":
            print("  Debes ingresar al menos un valor.\n")
            continue

        datos = []
        invalidos = []
        for valor in entrada.split(","):
            valor = valor.strip()
            if valor == "":
                continue  # ignora comas de más
            try:
                datos.append(float(valor))
            except ValueError:
                invalidos.append(valor)

        if invalidos:
            print(f"  Valores no válidos: {', '.join(invalidos)}. Intenta de nuevo.\n")
        elif not datos:
            print("  Debes ingresar al menos un valor.\n")
        else:
            return datos


# ---------- Funciones de formato para la tabla ----------

def fmt(n):
    """Muestra el número sin decimales innecesarios: 6.0 -> 6, 4.50 -> 4.5"""
    texto = f"{n:.2f}".rstrip("0").rstrip(".")
    return "0" if texto == "-0" else texto


def fp(n):
    """Como fmt, pero pone paréntesis a los negativos dentro de las fórmulas."""
    texto = fmt(n)
    return f"({texto})" if texto.startswith("-") else texto


def ancho(texto):
    """Ancho visible del texto (la barra de X̄ y Ȳ no ocupa espacio)."""
    return sum(1 for c in texto if not unicodedata.combining(c))


def centrar(texto, w):
    espacio = w - ancho(texto)
    izq = espacio // 2
    return " " * izq + texto + " " * (espacio - izq)


def imprimir_tabla(x, y):
    n = len(x)
    media_x = calcular_media(x)
    media_y = calcular_media(y)

    encabezados = ["Y", "X", "(X - X̄)²", "(X - X̄)(Y - Ȳ)"]

    filas = []
    for xi, yi in zip(x, y):
        dx = xi - media_x
        dy = yi - media_y
        col3 = f"({fmt(xi)} - {fp(media_x)})² = {fmt(dx ** 2)}"
        col4 = f"({fmt(xi)} - {fp(media_x)})({fmt(yi)} - {fp(media_y)}) = {fmt(dx * dy)}"
        filas.append([fmt(yi), fmt(xi), col3, col4])

    totales = [
        f"ΣY = {fmt(sum(y))}",
        f"ΣX = {fmt(sum(x))}",
        f"Σ(X - X̄)² = {fmt(suma_cuadrados(x, media_x))}",
        f"Σ(X - X̄)(Y - Ȳ) = {fmt(suma_productos(x, y, media_x, media_y))}",
    ]
    medias = [
        f"Ȳ = {fmt(sum(y))}/{n} = {fmt(media_y)}",
        f"X̄ = {fmt(sum(x))}/{n} = {fmt(media_x)}",
        "",
        "",
    ]

    # El ancho de cada columna se ajusta al texto más largo que contenga
    todas = [encabezados] + filas + [totales, medias]
    anchos = [max(ancho(fila[i]) for fila in todas) + 4 for i in range(4)]
    total = sum(anchos)

    def linea(celdas):
        return "".join(centrar(c, w) for c, w in zip(celdas, anchos))

    print()
    print("=" * total)
    print(linea(encabezados))
    print("=" * total)
    for fila in filas:
        print(linea(fila))
    print("-" * total)
    print(linea(totales))
    print(linea(medias))
    print("=" * total)


if __name__ == "__main__":
    y = pedir_datos("Y")

    while True:
        x = pedir_datos("X")
        if len(x) == len(y):
            break
        print(f"  Y tiene {len(y)} valores y X tiene {len(x)}. Deben tener la misma cantidad.\n")

    imprimir_tabla(x, y)


