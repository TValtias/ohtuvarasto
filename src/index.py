"""Main entry point for the application."""

from varasto import Varasto


def tulosta_luonti(mehua, olutta):
    """Prints stocks after creating them."""
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")


def tulosta_getterit(olutta):
    """Shows how much beer can fit"""

    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")


def kokeile_setterit(mehua):
    """Adds juice to stock and removes it."""

    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")


def kokeile_virheelliset_luonnit():
    """Creates stocks with incorrect values."""

    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)


def kokeile_lisaykset(mehua, olutta):
    """Tries too large and negative add."""

    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def kokeile_otot_liian_iso(olutta):
    """Tries a too large take."""

    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")

def kokeile_otot_negatiivinen(mehua):
    """Tries a negative take"""

    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def main():
    """Allows user to check the storage and to add and take from it"""

    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    tulosta_luonti(mehua, olutta)
    tulosta_getterit(olutta)
    kokeile_setterit(mehua)
    kokeile_virheelliset_luonnit()
    kokeile_lisaykset(mehua, olutta)
    kokeile_otot_liian_iso(olutta)
    kokeile_otot_negatiivinen(mehua)


if __name__ == "__main__":
    main()
