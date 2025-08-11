import pyshark

# Wczytaj plik PCAP
cap = pyshark.FileCapture('przechwycone_pakiety.pcapng', display_filter='http')

print("Wczytano plik PCAP.")

# Przejdź przez pakiety i znajdź pierwszy z nagłówkiem Authorization
for packet in cap:
    if hasattr(packet, 'http'):
        # Sprawdź, czy istnieje nagłówek Authorization
        if 'authorization' in packet.http.field_names:
            authorization_header = packet.http.authorization
            print("Authorization Header:", authorization_header)

            # Wyświetl całą zawartość pakietu
            print("\nCała zawartość pakietu:")
            print(packet)

            # Wyświetl tylko pierwszy pasujący pakiet
            break

cap.close()
